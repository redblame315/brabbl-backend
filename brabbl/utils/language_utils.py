from django.utils import translation
from django.utils.translation import ugettext as _


def set_language(request, lang):
    translation.activate(lang)
    request.LANGUAGE_CODE = translation.get_language()
    return request


def frontend_interface_messages():
    """
    Return list of all frontend's interface messages with translations.
    :return: dict
    """
    return {
        'language': translation.get_language(),
        'translations': {
            "User": _("User"),
            """Thank you for your registration!
            You will receive an email with a confirmation link.
            Once you click this, you can join the discussion.""": _(
                """Thank you for your registration!
                You will receive an email with a confirmation link.
                Once you click this, you can join the discussion."""
            ),
            "sort by date": _("sort by date"),
            "sort by personal review": _("sort by personal review"),
            "sorted by own rating": _(
                "sorted by own rating"
            ),
            "sort by average rating": _("sort by average rating"),
            "You must sign in to participate in the discussion": _(
                "You must sign in to participate in the discussion"
            ),
            "The profile has been updated successfully": _(
                "The profile has been updated successfully"
            ),
            "Choose topic": _("Choose topic"),
            "Profile": _("Profile"),
            "Logout": _("Logout"),
            "Register": _("Register"),
            "Login": _("Login"),
            "You have been logged out": _("You have been logged out"),
            "Come back soon!": _("Come back soon!"),
            "All discussions": _("All discussions"),
            "The argument has been changed": _(
                "The argument has been changed"
            ),
            "Great! Your argument is online now": _(
                "Great! Your argument is online now"
            ),
            "Edit discussion": _("Edit discussion"),
            "Edit Discussion": _("Edit Discussion"),
            "Create discussion": _("Create discussion"),
            "An email was sent with instructions on how to reset the password": _(
                "An email was sent with instructions on how to reset the password"
            ),
            "Edit suggestion": _("Edit suggestion"),
            "Report suggestion": _("Report suggestion"),
            "Add new suggestion": _("Add new suggestion"),
            "Add new Discussion": _("Add new Discussion"),
            "Add new Survey": _("Add new Survey"),
            "Update Discussion": _("Update Discussion"),
            "Add new pro-argument": _("Add new pro-argument"),
            "Add new contra-argument": _("Add new contra-argument"),
            "Edit argument": _("Edit argument"),
            "Publish argument": _("Publish argument"),
            "Publish Argument": _("Publish Argument"),
            "Edit survey": _("Edit survey"),
            "Edit Survey": _("Edit Survey"),
            "Add new survey": _("Add new survey"),
            "Survey": _("Survey"),
            "Discussion": _("Discussion"),
            "Tags": _("Tags"),
            "Settings": _("Settings"),
            "Create a new account": _("Create a new account"),
            "Forgot your password?": _("Forgot your password?"),
            "Please drag a picture to the image area to change your profile picture": _(
                "Please drag a picture to the image area to change your profile picture"
            ),
            "Please drag a picture to the image area to change discussion picture": _(
                "Please drag a picture to the image area to change discussion picture"
            ),
            "Reset Password": _("Reset Password"),
            "Update profile": _("Update profile"),
            "Already have an account?": _("Already have an account?"),
            "to": _("to"),
            "from": _("from"),
            "Edit": _("Edit"),
            "Add new": _("Add new"),
            "Cancel": _("Cancel"),
            "There was a server error": _("There was a server error"),
            "The action could not be carried out": _("The action could not be carried out"),
            "Please provide a subject": _("Please provide a subject"),
            "Please provide details for your argument": _(
                "Please provide details for your argument"
            ),
            "Just arguments": _("Just arguments"),
            "Just the Opiniometer": _("Just the Opiniometer"),
            "Opiniometer plus Arguments": _("Opiniometer plus Arguments"),
            "Thesis statement or question": _("Thesis statement or question"),
            "Please provide a thesis statement or question": _(
                "Please provide a thesis statement or question"
            ),
            "The thesis statement / question must not exceed 160 characters": _(
                "The thesis statement / question must not exceed 160 characters"
            ),
            "Please select the type of discussion": _(
                "Please select the type of discussion"
            ),
            "Please select the Opiniometer": _(
                "Please select the Opiniometer"
            ),
            "Please select the type of Opiniometer": _(
                "Please select the type of Opiniometer"
            ),
            "Allow suggestions by admins only": _(
                "Allow suggestions by admins only"
            ),
            "Allow suggestions by users": _("Allow suggestions by users"),
            "Please provide a (unique) username": _(
                "Please provide a (unique) username"
            ),
            "Please provide a password": _("Please provide a password"),
            "Please provide a fist name": _("Please provide a fist name"),
            "Please provide a last name": _("Please provide a last name"),
            "Please provide an email address": _(
                "Please provide an email address"
            ),
            "Please provide a valid email address": _(
                "Please provide a valid email address"
            ),
            "No email notifications": _("No email notifications"),
            "News e-mail (frequency)": _("News e-mail (frequency)"),
            "daily": _("daily"),
            "weekly": _("weekly"),
            "User name": _("User name"),
            "First name": _("First name"),
            "Last name": _("Last name"),
            "Email Address": _("Email Address"),
            "The passwords do not match": _("The passwords do not match"),
            "Password": _("Password"),
            "Please enter a password again": _(
                "Please enter a password again"
            ),
            "characters remaining": _("characters remaining"),
            "Average opinion": _("Average opinion"),
            "What do you think?": _("What do you think?"),
            "Argument": _("Argument"),
            "Reply": _("Reply"),
            "Replies": _("Replies"),
            "No suggestions yet": _("No suggestions yet"),
            "Thanks for reporting! We will review that content shortly": _(
                "Thanks for reporting! We will review that content shortly"
            ),
            "Thank you for your message": _("Thank you for your message"),
            "We will consider the amount shortly": _("We will consider the amount shortly"),
            "Hide proposal": _("Hide proposal"),
            "Edit proposal": _("Edit proposal"),
            "Report proposal": _("Report proposal"),
            "Add new argument": _("Add new argument"),
            "No arguments yet": _("No arguments yet"),
            "Start the discussion now!": _(" Start the discussion now!"),
            "Show more arguments": _("Show more arguments"),
            "Contra-Argument": _("Contra-Argument"),
            "Pro-Argument": _("Pro-Argument"),
            "Hide argument": _("Hide argument"),
            "Show argument": _("Show argument"),
            "Delete argument": _("Delete argument"),
            "Report argument": _("Report argument"),
            "Rate": _("Rate"),
            "powered by": _("powered by"),
            "DISCUSSION": _("DISCUSSION"),
            "inconsequential": _("inconsequential"),
            "questionable": _("questionable"),
            "justifiable": _("justifiable"),
            "relevant": _("relevant"),
            "convincingly": _("convincingly"),
            "Contra": _("Contra"),
            "Pro": _("Pro"),
            "Votes": _("Votes"),
            "Profile picture": _("Profile picture"),
            "Back": _("Back"),
            "cancel": _("cancel"),
            "create": _("create"),
            "change": _("change"),
            "Opinion": _("Opinion"),
            "Subject": _("Subject"),
            "Suggestion": _("Suggestion"),
            "Please enter a suggestion": _("Please enter a suggestion"),
            "by": _("by"),
            "All": _("All"),
            "Total": _("Total"),
            "Active": _("Active"),
            "Not Active": _("Not Active"),
            "Filter by status": _("Filter by status"),
            "Completed": _("Completed"),
            "Starts in": _("Starts in"),
            "Ends in": _("Ends in"),
            "Starts": _("Starts"),
            "Finishes": _("Finishes"),
            "d": _("d"),
            "h": _("h"),
            "m": _("m"),
            "s": _("s"),
            "Start Time": _("Start Time"),
            "End Time": _("End Time"),
            "Answer(s)": _("Answer(s)"),
            "very poor": _("very poor"),
            "poor": _("poor"),
            "ok": _("ok"),
            "good": _("good"),
            "very good": _("very good"),
            "CONTRA": _("CONTRA"),
            "PRO": _("PRO"),
            "Statement": _("Statement"),
            "Statements": _("Statements"),
            "Write new statement": _("Write new statement"),
            "Write new argument": _("Write new argument"),
            "Login with Facebook": _("Login with Facebook"),
            "Login with Twitter": _("Login with Twitter"),
            "Login with Google": _("Login with Google"),
            "Sign up with": _("Sign up with"),
            "Sign In": _("Sign In"),
            "or via mail": _("or via mail"),
            "Login to participate": _("Login to participate"),
            "Year of Birth": _("Year of Birth"),
            "Please provide a years of birth": _("Please provide a years of birth"),
            "Gender": _("Gender"),
            "Whatever": _("Whatever"),
            "Male": _("Male"),
            "Female": _("Female"),
            "Please provide a gender": _("Please provide a gender"),
            "Postcode": _("Postcode"),
            "Please provide a postcode": _("Please provide a postcode"),
            "Country": _("Country"),
            "Please provide a country": _("Please provide a country"),
            "City": _("City"),
            "Please provide a city": _("Please provide a city"),
            "Organization": _("Organization"),
            "Please provide a organization": _("Please provide a organization"),
            "Position": _("Position"),
            "Please provide a position": _("Please provide a position"),
            "Bundesland": _("Bundesland"),
            "Please provide a bundesland": _("Please provide a bundesland"),
            "Edit List": _("Edit List"),
            "Discussion List": _("Discussion List"),
            "Save List": _("Save List"),
            "Show all": _("Show all"),
            "Show sum of tags": _("Show sum of tags"),
            "Show intersection of tags": _("Show intersection of tags"),
            "List name": _("List name"),
            "Hide tag filter for Users": _("Hide tag filter for Users"),
            "Tag filter in the list view will not be shown to users": _(
                "Tag filter in the list view will not be shown to users"),
            "Please provide a list name": _("Please provide a list name"),
            "The list name must not exceed 160 characters": _("The list name must not exceed 160 characters"),
            "Content of list": _("Content of list"),
            "Please select the content of list": _("Please select the content of list"),
            "Please select the Wording schema": _("Please select the Wording schema"),
            "You can enter maximum of 4 digits": _("You can enter maximum of 4 digits"),
            "Add a tag": _("Add a tag"),
            "Press enter to add a tag": _("Press enter to add a tag"),
            "The discussion has not started yet": _("The discussion has not started yet"),
            "Write Pro-Argument": _("Write Pro-Argument"),
            "Write Contra-Argument": _("Write Contra-Argument"),
            "Update Argument": _("Update Argument"),
            "They were an email sent with instructions to reset the password":
                _("They were an email sent with instructions to reset the password"),
            "Add media": _("Add media"),
            "User list": _("User list"),
            "You can also upload an image or add a Youtube link": _(
                "You can also upload an image or add a Youtube link"),
            "Image": _("Image"),
            "Content removed": _("Content removed"),
            "This content was inappropriate and has been removed by our staff": _(
                "This content was inappropriate and has been removed by our staff"),
            "Please stick to our guidelines for good discussions and refrain from posts that are likely to be regarded "
            "as offensive or rude": _(
                "Please stick to our guidelines for good discussions and refrain from posts that are likely to be"
                " regarded as offensive or rude"),
            "User can add replies to arguments": _("User can add replies to arguments"),
            "Allow replies to arguments": _("Allow replies to arguments"),
            "Delete discussion": _("Delete discussion"),
            "Really delete this discussion? (This cannot be undone!)": _(
                "Really delete this discussion? (This cannot be undone!)"),
            "key_discussion-modal_textfield-title_description-of-discussion": _(
                "key_discussion-modal_textfield-title_description-of-discussion"),
            "key_discussion-modal_textfield-url_web-url-of-discussion": _(
                "key_discussion-modal_textfield-url_web-url-of-discussion"),
            "key_invite-participants-modal_title-of-invite-participants": _(
                "key_invite-participants-modal_title-of-invite-participants"),
            "key_invite-participants-modal_textfield-email_label": _(
                "key_invite-participants-modal_textfield-email_label"),
            "key_invite-participants-modal_textfield-email_help-text": _(
                "key_invite-participants-modal_textfield-email_help-text"),
            "key_invite-participants-modal_textfield-email_error-email": _(
                "key_invite-participants-modal_textfield-email_error-email"),
            "key_invite-participants-modal_textfield-email_error-emails": _(
                "key_invite-participants-modal_textfield-email_error-emails"),
            "key_invite-participants-modal_submit-button_label": _(
                "key_invite-participants-modal_submit-button_label"),
            "key_invite-participants-modal_invitation-list_revoke-invitation-hint": _(
                "key_invite-participants-modal_invitation-list_revoke-invitation-hint"),
            "key_invite-participants-modal_invitation-count-title": _(
                "key_invite-participants-modal_invitation-count-title"),
            "key_invite-participants-modal_alert_revoke-invitation-confirm": _(
                "key_invite-participants-modal_alert_revoke-invitation-confirm"),
            "key_survey-statement-options_edit": _("key_survey-statement-options_edit"),
            "key_survey-statement-options_report": _("key_survey-statement-options_report"),
            "key_signup_provide-password_title": _("key_signup_provide-password_title"),
            "key_signup_provide-password_error-text": _("key_signup_provide-password_error-text"),
            "key_signup_retype-password_title": _("key_signup_retype-password_title"),
            "key_signup_retype-password_error-text": _("key_signup_retype-password_error-text"),
            "key_login_email-textfield_error-text": _("key_login_email-textfield_error-text"),
            "accept_data_policy_overlay_not_checked_error": _("accept_data_policy_overlay_not_checked_error"),
            "key_discussion-modal_add-pdf-file_title": _("key_discussion-modal_add-pdf-file_title"),
            "key_discussion-modal_add-pdf-file_help": _("key_discussion-modal_add-pdf-file_help"),
            "key_discussion-modal_delete-pdf-hint": _("key_discussion-modal_delete-pdf-hint"),
            "key_discussion-modal_delete-pdf-confirm": _("key_discussion-modal_delete-pdf-confirm"),
            "key_discussion-modal_discussion-type-section_title": _(
                "key_discussion-modal_discussion-type-section_title"),
            "key_discussion-modal_discussion-type-section_pro-contra-discussion-name": _(
                "key_discussion-modal_discussion-type-section_pro-contra-discussion-name"),
            "statement-list-item_more-button-title": _("statement-list-item_more-button-title"),
            "statement-list-item_hide-button-title": _("statement-list-item_hide-button-title"),
            "arguments": _("arguments"),
            "key_discussion-options_edit": _("key_discussion-options_edit"),
            "key_discussion-options_delete": _("key_discussion-options_delete"),
            "key_survey-statement-options_delete": _("key_survey-statement-options_delete"),
            "Really delete this statement? (This cannot be undone!)": _(
                "Really delete this statement? (This cannot be undone!)"),
            "Delete statement": _("Delete statement"),
            "key_statement-modal_add-image_title": _(
                "key_statement-modal_add-image_title"),
            "key_statement-modal_add-image_help": _(
                "key_statement-modal_add-image_help"),
            "ADD PDF": _("ADD PDF"),
            "Add Photo": _("Add Photo"),
            "Add new idea": _("Add new idea"),
            "key_discussion_status_completed": _("key_discussion_status_completed"),
            "key_discussion_status_not_started": _("key_discussion_status_not_started"),
            "key_discussion_status_started": _("key_discussion_status_started"),
            "key_statement-modal_statement-title_title-label": _(
                "key_statement-modal_statement-title_title-label"),
            "key_statement-modal_statement-description_title-label": _(
                "key_statement-modal_statement-description_title-label"),
            "key_survey-statement-options_show": _("key_survey-statement-options_show"),
            "key_survey-statement-options_hide": _("key_survey-statement-options_hide"),
            "Now": _("Now"),
            "Active Forever": _("Active Forever"),
            "key_discussion-modal_discussion-type-help-text": _("key_discussion-modal_discussion-type-help-text"),
            "key_discussion-modal_start-time-help-text": _("key_discussion-modal_start-time-help-text"),
            "key_discussion-modal_end-time-help-text": _("key_discussion-modal_end-time-help-text"),
            "key_discussion-modal_textfield-url_web-url-of-discussion-help-text": _(
                "key_discussion-modal_textfield-url_web-url-of-discussion-help-text"),
            "key_discussion-modal_wording-help-text": _("key_discussion-modal_wording-help-text"),
            "key_discussion-modal_survey-option-help-text": _("key_discussion-modal_survey-option-help-text"),
            "key_discussion-modal_discussion-settings-help-text": _(
                "key_discussion-modal_discussion-settings-help-text"),
            "Advanced Options": _("Advanced Options"),
            "key_invite-participants_checkbox-is-admin-invitation": _(
                "key_invite-participants_checkbox-is-admin-invitation"),
            "Manage Participants": _("Manage Participants"),
            "key_discussion-modal_choose-private-label": _(
                "key_discussion-modal_choose-private-label"),
            "key_discussion-modal_choose-private_public-text": _(
                "key_discussion-modal_choose-private_public-text"),
            "key_discussion-modal_choose-private-help-text": _(
                "key_discussion-modal_choose-private-help-text"),
            "key_discussion-modal_participants-section-title": _(
                "key_discussion-modal_participants-section-title"),
            "key_discussion-modal_private-discussion-no-participants": _(
                "key_discussion-modal_private-discussion-no-participants"),
            "key_discussion-modal_public-discussion-text": _(
                "key_discussion-modal_public-discussion-text"),
            "key_discussion-modal_private-discussion-text": _(
                "key_discussion-modal_private-discussion-text"),
            "key_discussion-modal_choose-private_private-text": _(
                "key_discussion-modal_choose-private_private-text"),
            "key_user-menu_refresh-data": _("key_user-menu_refresh-data"),
            "key_barometer_disagree": _("key_barometer_disagree"),
            "key_barometer_agree": _("key_barometer_agree"),
            "key_barometer_behavior": _("key_barometer_behavior"),
            "key_barometer_always_show": _("key_barometer_always_show"),
            "key_barometer_show_only_for_voted_user": _("key_barometer_show_only_for_voted_user"),
            "key_barometer_show_only_for_voted_user_or_admin": _("key_barometer_show_only_for_voted_user_or_admin"),
            "key_discussion-modal_barometer-behavior-help-text": _("key_discussion-modal_barometer-behavior-help-text"),
            "key_discussion_statement-modal_textfield_copyright-info-label": _(
                "key_discussion_statement-modal_textfield_copyright-info-label"),
            "key_discussion_statement-modal_textfield_copyright-info-help-text": _(
                "key_discussion_statement-modal_textfield_copyright-info-help-text"),
            "key_discussion-options_reset": _("key_discussion-options_reset"),
            "Really remove barometer votes and argument ratings for this discussion? (This cannot be undone!)": _(
                "Really remove barometer votes and argument ratings for this discussion? (This cannot be undone!)"),
            "Reset discussion": _("Reset discussion"),
            "key_export_column_type": _("key_export_column_type"),
            "key_export_column_title": _("key_export_column_title"),
            "key_export_column_statement_title": _("key_export_column_statement_title"),
            "key_export_column_argument_title": _("key_export_column_argument_title"),
            "key_export_column_description": _("key_export_column_description"),
            "key_export_column_date_and_time_created": _("key_export_column_date_and_time_created"),
            "key_export_column_start_time": _("key_export_column_start_time"),
            "key_export_column_end_time": _("key_export_column_end_time"),
            "key_export_column_creator_name": _("key_export_column_creator_name"),
            "key_export_column_average_rating": _("key_export_column_average_rating"),
            "key_export_column_total_number_of_votes": _("key_export_column_total_number_of_votes"),
            "key_export_column_wording_for_plus_3_rating": _(
                "key_export_column_wording_for_plus_3_rating"),
            "key_export_column_number_of_votes_for_plus_3_rating": _(
                "key_export_column_number_of_votes_for_plus_3_rating"),
            "key_export_column_wording_for_plus_2_rating": _(
                "key_export_column_wording_for_plus_2_rating"),
            "key_export_column_number_of_votes_for_plus_2_rating": _(
                "key_export_column_number_of_votes_for_plus_2_rating"),
            "key_export_column_wording_for_plus_1_rating": _(
                "key_export_column_wording_for_plus_1_rating"),
            "key_export_column_number_of_votes_for_plus_1_rating": _(
                "key_export_column_number_of_votes_for_plus_1_rating"),
            "key_export_column_wording_for_0_rating": _(
                "key_export_column_wording_for_0_rating"),
            "key_export_column_number_of_votes_for_0_rating": _(
                "key_export_column_number_of_votes_for_0_rating"),
            "key_export_column_wording_for_minus_1_rating": _(
                "key_export_column_wording_for_minus_1_rating"),
            "key_export_column_wording_for_minus_2_rating": _(
                "key_export_column_wording_for_minus_2_rating"),
            "key_export_column_number_of_votes_for_minus_2_rating": _(
                "key_export_column_number_of_votes_for_minus_2_rating"),
            "key_export_column_wording_for_minus_3_rating": _(
                "key_export_column_wording_for_minus_3_rating"),
            "key_export_column_number_of_votes_for_minus_3_rating": _(
                "key_export_column_number_of_votes_for_minus_3_rating"),
            "key_export_client": _("key_export_client"),
            "key_export_date_and_time_of_export": _("key_export_date_and_time_of_export"),
            "key_export_discussion_modal_confirm_question": _(
                "key_export_discussion_modal_confirm_question"),
            "key_export_discussion_modal_btn_export": _(
                "key_export_discussion_modal_btn_export"),
            "key_discussion-options_export": _(
                "key_discussion-options_export"),
            "key_export_statistics": _("key_export_statistics"),
            "key_export_statistics_modal_confirm_question": _(
                "key_export_statistics_modal_confirm_question"),
            "key_export_statistics_modal_btn_export": _(
                "key_export_statistics_modal_btn_export"),
            "key_export_user_stats": _("key_export_user_stats"),
            "key_export_total_number_of_registered_users": _(
                "key_export_total_number_of_registered_users"),
            "key_export_number_of_users_in_age_group": _(
                "key_export_number_of_users_in_age_group"),
            "key_export_age_groups": _("key_export_age_groups"),
            "key_export_age_not_provided": _("key_export_age_not_provided"),
            "key_export_gender": _("key_export_gender"),
            "key_export_female_count": _("key_export_female_count"),
            "key_export_male_count": _("key_export_male_count"),
            "key_export_gender_not_provided": _("key_export_gender_not_provided"),
            "key_export_post_code": _("key_export_post_code"),
            "key_export_post_code_not_provided": _("key_export_post_code_not_provided"),
            "key_export_city": _("key_export_city"),
            "key_export_city_not_provided": _("key_export_city_not_provided"),
            "key_export_organization": _("key_export_organization"),
            "key_export_organization_not_provided": _("key_export_organization_not_provided"),
            "key_export_position": _("key_export_position"),
            "key_export_position_not_provided": _("key_export_position_not_provided"),
            "key_export_participation": _("key_export_participation"),
            "key_export_number_of_discussions": _("key_export_number_of_discussions"),
            "key_export_number_of_statements": _("key_export_number_of_statements"),
            "key_export_number_of_arguments": _("key_export_number_of_arguments"),
            "key_export_number_of_barometer_voting": _("key_export_number_of_barometer_voting"),
            "key_export_users_with_position": _("key_export_users_with_position"),
            "key_export_users_with_organization": _("key_export_users_with_organization"),
            "key_export_users_with_city": _("key_export_users_with_city"),
            "key_export_users_with_post_code": _("key_export_users_with_post_code")
        }
    }
