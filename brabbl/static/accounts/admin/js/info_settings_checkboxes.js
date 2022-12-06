django.jQuery(document).ready(function () {
  django.jQuery('#model_properties-group input[type="checkbox"]').change(function () {
    if (django.jQuery(this).is(':checked')) {
      django.jQuery(this).closest('td').prevAll('td').find('input[type="checkbox"]').prop('checked', true);
    } else {
      django.jQuery(this).closest('td').nextAll('td').find('input[type="checkbox"]').prop('checked', false);
    }
  });
});
