$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    var modal = $("#"+btn.attr("data-contener-id"))
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        modal.modal("show");
      },
      success: function (data) {
        modal.find(".modal-content").html(data.html_form);
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
          $(this).closest(".modal").modal("hide")
          location.reload();
        }
        else {
          $(this).closest(".modal").find(".modal-content").html(data.html_form);
          console.log(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */
    /* Fuel Reservation*/
  $("#reservation_table").on("click", ".js-update-fuel-served", loadForm);
  $("#modal-update-fuel").on("submit", ".js-fuel-served-update-form", saveForm);


  /* Pilot Reservation*/
$("#add_ulm_btn").on("click", ".js-add-ulm", loadForm);
$("#modal-add-ulm").on("submit", ".js-add-ulm-form", saveForm);

$("#reservation_table").on('click', '.js-update-reservation', loadForm)
$("#modal-update-reservation").on("submit", ".js-staff-update-reservation-form", saveForm)

});
