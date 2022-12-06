django.jQuery(document).ready(function () {
  disable_selected_options();
  django.jQuery('.field-key').change(function () {
    disable_selected_options();
  });
});

function disable_selected_options() {
  django.jQuery('div.field-key option').attr('disabled', false);
  django.jQuery('div.field-key select option:selected').each(function () {
    django.jQuery('div.field-key option:not(:selected)[value="' + django.jQuery(this).val() + '"]').attr('disabled', 'disabled');
  });
}
