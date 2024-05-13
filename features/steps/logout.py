from behave import *

use_step_matcher("parse")

@when('I click on the "Logout" button')
def step_when_click_logout(context):
    logout_button = context.browser.find_by_css('.genericButton.logoutButton')
    logout_button.click()


@then('I should be redirected to the "Login" page')
def step_then_redirected_to_login(context):
    login_button = context.browser.find_by_css('.genericButton.loginButton')
    login_button.click()
    assert context.browser.url.endswith('/accounts/login/'), 'No se redirigió a la página de inicio de sesión'