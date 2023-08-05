# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.pivot -t test_Family.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.pivot.testing.COLLECTIVE_PIVOT_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/collective/pivot/tests/robot/test_Family.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Family
  Given a logged-in site administrator
    and an add Family form
   When I type 'My Family' into the title field
    and I submit the form
   Then a Family with the title 'My Family' has been created

Scenario: As a site administrator I can view a Family
  Given a logged-in site administrator
    and a Family 'My Family'
   When I go to the Family view
   Then I can see the Family title 'My Family'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Family form
  Go To  ${PLONE_URL}/++add++Family

a Family 'My Family'
  Create content  type=Family  id=my-Family  title=My Family

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Family view
  Go To  ${PLONE_URL}/my-Family
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Family with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Family title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
