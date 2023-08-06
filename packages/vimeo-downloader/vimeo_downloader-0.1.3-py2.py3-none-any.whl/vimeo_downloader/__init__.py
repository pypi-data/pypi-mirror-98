"""
Downloads Vimeo videos and retrieve metadata such as views, likes, comments, duration.

Features
    * Easy to use and friendly API.
    * Support for downloading private or embed only Vimeo videos.
    * Retrieve direct URL for the video file.
Usage:
    >>> from vimeo_downloader import Vimeo
    >>> v = Vimeo('https://vimeo.com/503166067')
    >>> meta = v.metadata
    >>> s = v.streams
    >>> s
        [Stream(240p), Stream(360p), Stream(540p), Stream(720p), Stream(1080p)]
    >>> best_stream = s[-1] # Select the best stream
    >>> best_stream.filesize
    '166.589421 MB'
    >>> best_stream.direct_url
    'https://vod-progressive.akamaized.net.../2298326263.mp4'
    >>> best_stream.download(download_directory='DirectoryName',filename='FileName')
    # For private or embed only videos
    >>> v = Vimeo('https://player.vimeo.com/video/498617513',
                  embedded_on='https://atpstar.com/plans-162.html') 
"""

import requests
import re
from collections import namedtuple
from tqdm import tqdm
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
}
config = "https://player.vimeo.com/video/{}/config"
details = "http://vimeo.com/api/v2/video/{}.json"


class URLNotSupported(Exception):
    pass


class RequestError(Exception):
    pass


class UnableToParseHtml(Exception):
    pass


class URLExpired(RequestError):
    pass


class _Stream:
    """
    Downloads mp4 files from vimeo as used by :class:`Vimeo`.

    Attributes:
        direct_url : str
            direct URL for the mp4 file 
        filesize : str
            Total size of file in MB
        quality : str
            Quality of the stream

    Method:
        download(download_directory = '', filename = None, mute = False)
    """

    def __init__(self, direct_url: str, quality: str):
        self._direct_url = direct_url  # Direct url for the mp4 file
        self._quality = quality  # Quality of the stream

    def __repr__(self):
        return f'Stream({self._quality})'

    def __len__(self):
        return self.filesize

    def __lt__(self, other):
        """
        Streams are sortable based on quality
        """
        return int(self._quality[:-1]) < int(other._quality[:-1])

    @property
    def direct_url(self):
        return self._direct_url

    @property
    def quality(self):
        return self._quality

    def download(self, download_directory: str = '', filename: str = None, mute: bool = False):
        """Downloads the video with progress bar if `mute=False`

        Args:
            download_directory (str, optional): Download directory for the video. Defaults to ''.
            filename (str, optional): File name with which video is saved. Defaults to None.
            mute (bool, optional): If it is False progress bar, download speed and ETA is displayed. Defaults to False.
        """

        if filename is None:
            try:
                filename = re.findall(
                    r'\/(\d+\.mp4|webm$)', self._direct_url)[0]
            except IndexError:
                filename = f'{self._quality}.mp4'
        else:
            filename += '.mp4'
        r = requests.get(self._direct_url, stream=True, headers=headers)
        if not r.ok:
            if r.status_code == 410:
                raise URLExpired('The download URL has expired.')
            raise RequestError(f'{r.status_code}: Unable to fetch the video.')
        dp = os.path.join(download_directory, filename)
        if download_directory:
            if not os.path.isdir(download_directory):
                os.makedirs(download_directory)
        with open(dp, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            chunk_size = 1024
            if not mute:
                for chunk in tqdm(iterable=r.iter_content(chunk_size=chunk_size), total=total_length//chunk_size,
                                  unit='KB', desc=filename):
                    if chunk:
                        f.write(chunk)
                        f.flush()
            else:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()

    @property
    def filesize(self):
        """
        Returns:
            str: Returns file size of the video in MB
        """

        r = requests.get(self._direct_url, stream=True, headers=headers)
        return (str(int(r.headers.get('content-length'))/10**6) + ' MB')


class Vimeo:

    """
    This is for fetching meta data and returns :class:`_Stream` object which could be used to download videos.

    Attributes:
        metadata
            namedtuple containing meta data
        streams : list
            List containing all available qualities
    """

    def __init__(self, url: str, embedded_on: str = None):
        """
        Args:
            url (str): URL of the vimeo video without any query parameters
            embedded_on (str, optional): Only neccessary if the video is embed only. 
                                         URL of the site on which the video is embedded on, without any query parameters. 
                                         Defaults to None.
        """

        self._url = url  # URL for the vimeo video
        self._video_id = self._validate_url()  # Video ID at the end of the link
        self._headers = headers
        if embedded_on:
            self._headers['Referer'] = embedded_on

    def _validate_url(self):
        """It validates if the URL is of Vimeo and returns the video ID

        Returns:
            str: Video ID of the video
        """

        accepted_pattern = [
            r'^https:\/\/player.vimeo.com\/video\/(\d+)$', r'^https:\/\/vimeo.com\/(\d+)$']
        for pattern in accepted_pattern:
            match = re.findall(pattern, self._url)
            if match:
                return match[0]
        # If none of the patterns is matched exception is raised
        raise URLNotSupported(
            f'{self._url} is not supported. Make sure you don\'t include query parameters in the url')

    def _extractor(self):
        """Extracts the direct mp4 link for the vimeo video

        Returns:
            dict: JSON data with URL information
        """

        js_url = requests.get(config.format(self._video_id),
                              headers=self._headers)

        if not js_url.ok:
            if js_url.status_code == 403:
                # If the response is forbidden it tries another way to fetch link
                html = requests.get(self._url, headers=self._headers)
                if html.ok:
                    try:
                        url = config.format(
                            self._video_id).replace('/', r'\\/')
                        pattern = '"({}.+?)"'.format(url)

                        request_conf_link = re.findall(pattern, html.text)[
                            0].replace(r'\/', '/')

                        js_url = requests.get(
                            request_conf_link, headers=self._headers)
                        return js_url.json()
                    except IndexError:
                        raise UnableToParseHtml('Couldn\'t find config url')

                else:
                    if html.status_code == 403:
                        raise RequestError(
                            (f'{html.status_code}: If the video is embed only, also provide the url '
                             'on which it is embedded, Vimeo(url=<vimeo_url>,embedded_on=<url>)'))
                    else:
                        raise RequestError(
                            f'{html.status_code}: Unable to retrieve download links')
            else:
                raise RequestError(
                    f'{js_url.status_code}: Unable to retrieve download links')
        try:
            js_url = js_url.json()
        except Exception as e:
            raise RequestError(f'Couldn\'t retrieve download links: {e}')
        return js_url

    def _get_meta_data(self):
        """Retrieves meta data for the video

        Returns:
            dict: JSON data containing meta information
        """

        video_info = requests.get(
            details.format(self._video_id), headers=self._headers)
        if not video_info.ok:
            raise RequestError(
                f'{video_info.status_code}: Unable to retrieve meta data.')
        try:
            video_info = video_info.json()
        except Exception as e:
            raise RequestError(f'Couldn\'t retrieve meta data: {e}')
        return video_info

    @property
    def metadata(self):
        """
        Fetch metadata and return it in form of namedtuple.
        """

        self._meta_data = self._get_meta_data()[0]
        try:
            self._meta_data['likes'] = self._meta_data.pop(
                "stats_number_of_likes")
            self._meta_data['views'] = self._meta_data.pop(
                "stats_number_of_plays")
            self._meta_data['number_of_comments'] = self._meta_data.pop(
                "stats_number_of_comments")
        except KeyError:
            pass
        metadata = namedtuple('Metadata', self._meta_data.keys())
        return metadata(**self._meta_data)

    @property
    def streams(self) -> list:
        """Get all available streams for a video

        Returns:
            list: Return :class:`_Stream` objects in list
        """

        js_url = self._extractor()
        dl = []
        for stream in js_url['request']['files']['progressive']:
            dl.append(
                _Stream(quality=stream['quality'], direct_url=stream['url']))
        dl.sort()
        return dl

    def __repr__(self):
        return f'Vimeo<{self._url}>'
