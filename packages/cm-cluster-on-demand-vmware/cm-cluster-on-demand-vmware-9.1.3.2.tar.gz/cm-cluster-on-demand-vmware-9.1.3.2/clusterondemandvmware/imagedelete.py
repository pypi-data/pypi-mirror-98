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

from __future__ import absolute_import

import logging

from clusterondemand.clustercreate import generate_cluster_tags, generate_uuid_tag
from clusterondemand.images.find import findimages_ns
from clusterondemand.images.utils import flatten_images
from clusterondemand.utils import confirm, confirm_ns
from clusterondemandconfig import ConfigNamespace, config

from . import clientutils
from .configuration import vmwarecommon_ns
from .imageinstall import make_image_tags
from .images import VMWareImageSource
from .utils import print_images_table

log = logging.getLogger("cluster-on-demand")


config_ns = ConfigNamespace("vmware.image.delete", help_section="image delete parameters")
config_ns.import_namespace(vmwarecommon_ns)
config_ns.import_namespace(findimages_ns)
config_ns.import_namespace(confirm_ns)
config_ns.add_switch_parameter(
    "dry_run",
    help="Don't actually remove images. Just output log entries."
)


def head_nodes_using_image(head_image):
    assert head_image.type == "headnode"

    sm = clientutils.get_service_manager()

    tag_id = sm.get_tag_id(generate_uuid_tag(head_image))
    tag_id_to_objs = sm.vsphere.tagging.TagAssociation.list_attached_objects_on_tags([tag_id])

    vm_names = [
        f"{obj.type}:{obj.id}"
        for item in tag_id_to_objs
        for obj in item.object_ids
        if obj.id != head_image.uuid    # The image itself will always have the tag
    ]
    return vm_names


def delete_unused_tags(image):
    sm = clientutils.get_service_manager()

    all_tags = generate_cluster_tags(image, only_image_tags=True) + make_image_tags(image)
    tag_ids_map = sm.get_tag_ids_map(all_tags)

    tag_id_to_objs = sm.vsphere.tagging.TagAssociation.list_attached_objects_on_tags(tag_ids_map.keys())

    for item in tag_id_to_objs:
        tag_id = item.tag_id
        tag_name = tag_ids_map[tag_id]
        # This function is called just after the image was deleted. Unfortunately vSphere is slow to propagate this,
        # So 'list_attached_objects_on_tags' may also return this image as one of the attachments.
        # So let's ignore attachments to image.uuid
        objects = [obj for obj in item.object_ids if obj.id != image.uuid]

        if not objects:
            log.info(f"Deleting tag {tag_name}")
            sm.vsphere.tagging.Tag.delete(tag_id)
        else:
            log.debug(f"Tag {tag_name} is attached to {len(objects)} objects")


def run_command():
    log.info("Finding images...")

    images = list(VMWareImageSource.find_images_using_options(config))
    images_to_delete = []

    # We only delete images that are not in use. Otherwise, it's impossible to clear unused tags as they are being
    # used by the cluster.
    # The cluster tags cannot be deleted on "cluster delete" because the users may not have admin permissions.
    for image in images:
        vms = head_nodes_using_image(image)
        if vms:
            log.info(f"The image {image.name} is being used by: {', '.join(vms)}. "
                     f"Please delete those before deleting this image")
        else:
            images_to_delete.append(image)

    print_images_table(flatten_images(images_to_delete))
    if not confirm("About to delete these images"):
        return

    if config["dry_run"]:
        log.info("Images won't be deleted because of dry-run mode")
        return

    for image in flatten_images(images_to_delete):
        try:
            log.info(f"Removing {image. type} image {image.id}:{image.revision} ({image.name})")
            clientutils.get_service_manager().vsphere.content.library.Item.delete(image.uuid)
            log.info(f"Deleting unused tags for image {image.name}")
            delete_unused_tags(image)
        except Exception as e:
            log.error(f"Failed to remove a {image.type} image {image.id}:{image.revision}: {e}")

    log.info("Done")
