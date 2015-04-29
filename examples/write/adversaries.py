""" standard """
from random import randint
import re

""" custom """
from examples.working_init import *


def main():
    """ """
    # This is a random number generator used for testing.
    randy = randint(1, 1000)

    # (Required) Instantiate a Resource Object
    resources = tc.adversaries()

    # (Optional) Filters can be added here if required to narrow the result set.
    # filter1 = resources.add_filter()

    # (Optional) retrieve all results
    resources.retrieve()

    # (Optional) iterate through all results if retrieve was used above
    for res in resources:

        # (Optional) match a particular resource by ID, Name or any other supported attribute.
        # testdev
        # if res.get_id() == 747266:
        if res.get_id() == 3:
            #
            # update resource if required
            #
            res.set_name('Loop Update Adversary Sample {0}'.format(randy))

            #
            # working with indicator associations
            #

            # (Optional) get all indicator associations
            # resources.get_indicator_associations(res)
            resources.get_indicator_associations(res, IndicatorType.EMAIL_ADDRESSES)
            for association in res.association_objects_indicators:
                # add delete flag to all indicator association that have a confidence under 10
                if association.get_confidence() < 10:
                    res.disassociate(association.resource_type, association.get_indicator())

            res.associate(ResourceType.EMAIL_ADDRESSES, 'bcs_bad_guy@badguysareus.com')

            #
            # working with group associations
            #

            # (Optional) get all group associations
            resources.get_group_associations(res)
            for association in res.association_objects_groups:
                # add delete flag to all group association that match DELETE
                if re.findall('Loop', association.get_name()):
                    res.disassociate(association.resource_type, association.get_id())

            res.associate(ResourceType.EMAILS, 747227)

            #
            # working with victim associations
            #

            # (Optional) get all victim associations
            resources.get_victim_associations(res)
            for association in res.association_objects_victims:
                print(association)
                # add delete flag to all group association that match DELETE
                # if re.findall('Loop', association.get_name()):
                #     res.disassociate(association.resource_type, association.get_id())

            # res.associate(ResourceType.VICTIMS, 747266)

            #
            # working with attributes
            #

            # (Optional) get all attributes associated with this resource
            resources.get_attributes(res)
            for attribute in res.attribute_objects:
                # add delete flag to all attributes that have 'test' in the value.
                if re.findall('test', attribute.get_value()):
                    res.delete_attribute(attribute.get_id())
                # add update flag to all attributes that have 'update' in the value.
                if re.findall('update', attribute.get_value()):
                    res.update_attribute(attribute.get_id(), 'updated attribute {0}'.format(randy))
            # (Optional) add attribute to resource with type and value
            res.add_attribute('Description', 'test attribute {0}'.format(randy))

            #
            # working with tags
            #

            # (Optional) get all tags associated with this resource
            resources.get_tags(res)
            for tag in res.tag_objects:
                # add delete flag to all tags that have 'DELETE' in the name.
                if re.findall('DELETE', tag.get_name()):
                    res.delete_tag(tag.get_name())
            # (Optional) add tag to resource
            res.add_tag('DELETE_{0}'.format(randy))
        #
        # delete resource if required
        #

        # (Optional) add delete flag to any resource that has 'DELETE' in the name.
        if re.findall('DELETE', res.get_name()):
            res.delete()

    #
    # add resource if required
    #
    resource = resources.add('DELETE {0}'.format(randy))

    # (Optional) add attribute to newly created resource
    resource.add_attribute('Description', 'test attribute {0}'.format(randy))

    # (Optional) add tag to newly created resource
    resource.add_tag('TAG {0}'.format(randy))

    #
    # update resource if required
    #

    # (Optional) a resource can be updated directly by using the resource id.
    # resource = resources.update(749422)
    resource = resources.update(4)
    resource.set_name('Manual Update Adversary Sample {0}'.format(randy))

    # (Optional) add attribute to newly created resource
    resource.add_attribute('Description', 'test attribute {0}'.format(randy))

    # (Optional) add tag to newly created resource
    resource.add_tag('TAG {0}'.format(randy))

    #
    # delete resource
    #

    # (Optional) a resource can be deleted directly by using the resource id.
    # resources.delete(752422)

    # (Required) commit all changes above.  No changes are made until the commit phase.
    resources.commit()

    # (Optional) iterate through the result sets after changes.
    for res in resources:
        print(res)

    # (Optional) display a commit report of all API actions performed
    print(tc.report)

    for rpt in tc.report:
        print(rpt)


if __name__ == "__main__":
    main()
    sys.exit()
