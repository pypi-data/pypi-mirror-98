from .get_shape import get_shape, get_service
import json
import logging

logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)


def xml_etree_to_dict(elm, service=None, shape=None, level=1):
    """

    Traverse a python ElementTree and using the AWS shapes, construct
    a dict. Recursive method.
    
    This method was built iteratively by testing against the test suite
    and is pretty messy. Recommendations for clean up:
    * Use dataclasses for representing all these dicts
    * Make the logging more verbose and explicit
    
    """
    if service is None:
        service = get_service(elm.tag)

    shape = shape or get_shape(elm.tag, service=service)
    logger.debug(">" * level + " " + elm.tag + " " + json.dumps(shape))
    if shape is None:
        d = {}
        for child in elm:
            child_d = xml_etree_to_dict(child, service=service, level=level + 1)
            if not isinstance(child_d, dict):
                d.update({child.tag: child_d})
            else:
                d.update(child_d)
        return {elm.tag: d}

    if shape == "String" or shape["type"] == "string":
        return elm.text
    elif shape["type"] == "structure":
        d = {}
        for member_name, member_metadata in shape["members"].items():
            member_shape = get_shape(member_metadata["shape"], service=service)
            logger.debug(
                ">" * level + "(m) " + member_name + " " + json.dumps(member_shape)
            )
            if member_shape["type"] == "list":
                # we lowercase the first letter for lists by AWS Accept: application/json convention
                list_key = member_name[0].lower() + member_name[1:]
                d[list_key] = []
                for child in elm:
                    if child.tag == member_shape["member"]["locationName"]:
                        d[list_key].append(
                            xml_etree_to_dict(
                                child,
                                service=service,
                                shape=get_shape(
                                    member_shape["member"]["shape"], service=service
                                ),
                                level=level + 1,
                            )
                        )
            elif member_shape["type"] == "structure":
                d[member_name] = xml_etree_to_dict(
                    elm.find(member_metadata["locationName"]),
                    service=service,
                    shape=member_shape,
                    level=level + 1,
                )
            elif member_shape["type"] == "string" or member_shape["type"] == "blob":
                try:
                    d[member_name] = elm.find(member_name).text.strip()
                except AttributeError:
                    pass
            elif member_shape["type"] == "map":
                if "locationName" not in member_shape:
                    map_elms = elm.findall("Attribute")
                else:
                    map_elms = elm.findall(member_shape["locationName"])
                for map_elm in map_elms:
                    key_elm = map_elm.find(member_shape["key"]["locationName"])
                    # if not key_elm:
                    #     continue
                    key = key_elm.text
                    val_elm = map_elm.find(member_shape["value"]["locationName"])
                    d[key] = xml_etree_to_dict(
                        val_elm,
                        service=service,
                        shape="String",
                        # shape=get_shape(
                        #     member_shape["value"]["shape"], service=service
                        # ),
                        level=level + 1,
                    )
            else:
                logger.warning(
                    f'Unknown shape type "{member_shape["type"]}" for {member_name}'
                )
        return {elm.tag: d}
    return {}