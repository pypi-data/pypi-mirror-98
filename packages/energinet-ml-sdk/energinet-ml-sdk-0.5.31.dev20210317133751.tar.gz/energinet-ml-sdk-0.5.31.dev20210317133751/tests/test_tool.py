from energinetml.core.project import Project


def test_tool():

    project = Project(
        path='path',
        name='name',
        subscription_id='subscription_id',
        resource_group='resource_group',
        workspace_name='workspace_name',
        location='location',
    )

    assert project.vnet_resourcegroup_name == 'resource_group'
