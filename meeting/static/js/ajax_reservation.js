$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-fuel-served").modal("show");
      },
      success: function (data) {
        console.log(data)
        $("#modal-fuel-served .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-fuel-served").modal("hide");
        }
        else {
          $("#modal-fuel-served .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */
  $("#reservation_table").on("click", ".js-update-fuel-served", loadForm);
  $("#modal-fuel-served").on("submit", ".js-fuel-served-update-form", saveForm);

});
