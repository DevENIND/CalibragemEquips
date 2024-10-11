function abreModal() {
  $("#ExemploModalCentralizado").modal({
    show: true
  });
}

setTimeout(abreModal, 1000);

$(window).load(function() {
    $('#exemplomodal').modal('show');
});