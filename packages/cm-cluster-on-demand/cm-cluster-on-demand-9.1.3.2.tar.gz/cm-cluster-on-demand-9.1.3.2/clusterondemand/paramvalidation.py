# Copyright 2004-2021 Bright Computing Holding BV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
from logging import getLogger

from .exceptions import ValidationException
from .utils import is_valid_cluster_name

UUID_REGEX = "^[0-9a-fA-F]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$"
PRODUCT_KEY_REGEX = "^[0-9]{6}(-[0-9]{6}){4}$"
_IMAGE_NAME_REGEX = r"[^-]+"
_BCM_VERSION_REGEX = r"(?:trunk|\d+\.\d+)(?:-[a-z-]+[a-z])?"
_IMAGE_REVISION_REGEX = r"\d+"
VALID_IMAGE_REGEX = r"^(?!bcmn|bcmh)%s-%s:%s$" % (_IMAGE_NAME_REGEX, _BCM_VERSION_REGEX, _IMAGE_REVISION_REGEX)
VALID_HEADNODE_IMAGE_REGEX = r"^bcmh-%s-%s-%s$" % (_IMAGE_NAME_REGEX, _BCM_VERSION_REGEX, _IMAGE_REVISION_REGEX)
VALID_NODE_IMAGE_REGEX = r"^bcmn-%s-%s-%s$" % (_IMAGE_NAME_REGEX, _BCM_VERSION_REGEX, _IMAGE_REVISION_REGEX)

log = getLogger("cluster-on-demand")


# TODO Get rid of this class and put in functions?
# There is no point in having a class with only static methods
class ParamValidator(object):

    @staticmethod
    def validate_cluster_name(cluster_name):
        if not is_valid_cluster_name(cluster_name):
            raise ValidationException(
                f"The cluster name '{cluster_name}' does not match the proper format. "
                f"The cluster name cannot exceed 64 characters in length and "
                f"should be a valid hostname as specified by RFC952 and RFC1123."
            )

    @staticmethod
    def validate_uuid_format(uuid_string, error_message=""):
        if not error_message:
            error_message = f"{uuid_string} is not a valid UUID"

        if not bool(re.match(UUID_REGEX, uuid_string)):
            raise ValidationException(error_message)

    @staticmethod
    def validate_license_product_key(parameter, configuration):
        product_key_string = configuration[parameter.key]

        if not re.match(PRODUCT_KEY_REGEX, product_key_string):
            raise ValidationException("License product key does not match the proper format")


def validate_image_value(parameter, config):
    value = config[parameter.key]
    if value and not re.match(VALID_IMAGE_REGEX, value):
        log.warn(f"'{value}' does not seem to be a valid image. "
                 "Expected format <distro>-<bcm version>:<n>, e.g. 'ubuntu1604-trunk:13'")


def validate_headnode_image_value(parameter, config):
    value = config[parameter.key]
    if value and not re.match(VALID_HEADNODE_IMAGE_REGEX, value):
        log.warn(f"'{value}' does not seem to be a valid head node image. "
                 "Expected format bcmh-<distro>-<bcm version>-<n>, e.g. 'bcmh-ubuntu1604-trunk-13'")


def validate_node_image_value(parameter, config):
    value = config[parameter.key]
    if value and not re.match(VALID_NODE_IMAGE_REGEX, value):
        log.warn(f"'{value}' does not seem to be a valid node image. "
                 "Expected format bcmn-<distro>-<bcm version>-<n>, e.g. 'bcmn-ubuntu1604-trunk-13'")
