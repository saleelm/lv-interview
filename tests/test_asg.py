import pytest
import os
from asg_helper.asg import ASGHelper

@pytest.fixture
def asg_instance():
    """
    Fixture to create an ASGHelper instance for testing.

    Returns:
        ASGHelper: An instance of ASGHelper.
    """
    region = os.getenv('AWS_REGION')
    access_key = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    asg = ASGHelper(region, access_key, secret_key)
    return asg


def test_validate_asg_running_count(asg_instance):
    """
    Test the validate_asg_running_count function.

    Args:
        asg_instance (ASGHelper): An instance of ASGHelper.
    """
    assert asg_instance.validate_asg_running_count() == True

def test_validate_az_distribution(asg_instance):
    """
    Test the validate_az_distribution function.

    Args:
        asg_instance (ASGHelper): An instance of ASGHelper.
    """
    assert asg_instance.validate_az_distribution() == True

@pytest.mark.saleel
def test_validate_instance_properties(asg_instance):
    """
    Test the validate_instance_properties function.

    Args:
        asg_instance (ASGHelper): An instance of ASGHelper.
    """
    assert asg_instance.validate_instance_properties() == True

def test_get_longest_running_instance_uptime(asg_instance):
    """
    Test the get_longest_running_instance_uptime function.

    Args:
        asg_instance (ASGHelper): An instance of ASGHelper.
    """
    uptime = asg_instance.get_longest_running_instance_uptime()
    assert uptime is not None

def test_get_scheduled_actions(asg_instance):
    """
    Test the get_scheduled_actions function.

    Args:
        asg_instance (ASGHelper): An instance of ASGHelper.
    """
    actions = asg_instance.get_scheduled_actions()
    assert actions is not None

def test_calculate_elapsed_time(asg_instance):
    """
    Test the calculate_elapsed_time function.

    Args:
        asg_instance (ASGHelper): An instance of ASGHelper.
    """
    actions = asg_instance.get_scheduled_actions()
    elapsed_time = asg_instance.calculate_elapsed_time(actions)
    assert elapsed_time is not None

def test_get_instances_launched_terminated_today(asg_instance):
    """
    Test the get_instances_launched_terminated_today function.

    Args:
        asg_instance (ASGHelper): An instance of ASGHelper.
    """
    activities = asg_instance.get_instances_launched_terminated_today()
    assert activities is not None
