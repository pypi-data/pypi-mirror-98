from __future__ import absolute_import

from . import BaseProxy
from ..requests import Request, munchify
from ..helpers import for_all_methods, bind_proxy


@for_all_methods(bind_proxy)
class BuildChrootProxy(BaseProxy):
    def get(self, build_id, chrootname):
        """
        Return a build chroot

        :param int build_id:
        :param str chrootname:
        :return: Munch
        """
        endpoint = "/build-chroot"
        params = {
            "build_id": build_id,
            "chrootname": chrootname,
        }
        request = Request(endpoint, api_base_url=self.api_base_url, params=params)
        response = request.send()
        return munchify(response)

    def get_list(self, build_id, pagination=None):
        """
        Return a list of build chroots

        :param int build_id:
        :param str chrootname:
        :param pagination:
        :return: Munch
        """
        endpoint = "/build-chroot/list"
        params = {
            "build_id": build_id,
        }
        params.update(pagination or {})
        request = Request(endpoint, api_base_url=self.api_base_url, params=params)
        response = request.send()
        return munchify(response)

    def get_build_config(self, build_id, chrootname):
        """
        Return a build config for a build chroot

        :param int build_id:
        :param str chrootname:
        :return: Munch
        """
        endpoint = "/build-chroot/build-config"
        params = {
            "build_id": build_id,
            "chrootname": chrootname,
        }
        request = Request(endpoint, api_base_url=self.api_base_url, params=params)
        response = request.send()
        return munchify(response)
