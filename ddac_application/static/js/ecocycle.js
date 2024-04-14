
'use strict';
$(document).ready(function() {

    // Accordion
    var all_panels = $('.ecocycle-accordion > li > ul').hide();

    $('.ecocycle-accordion > li > a').click(function() {
        console.log('Hello world!');
        var target =  $(this).next();
        if(!target.hasClass('active')){
            all_panels.removeClass('active').slideUp();
            target.addClass('active').slideDown();
        }
      return false;
    });
    // End accordion

    // Product detail
    $('.product-links-wap a').click(function(){
      var this_src = $(this).children('img').attr('src');
      $('#product-detail').attr('src',this_src);
      return false;
    });
    $('#btn-minus').click(function(){
      var val = $("#var-value").html();
      val = (val=='1')?val:val-1;
      $("#var-value").html(val);
      $("#product-quanity").val(val);
      return false;
    });
    $('#btn-plus').click(function(){
      var val = $("#var-value").html();
      val++;
      $("#var-value").html(val);
      $("#product-quanity").val(val);
      return false;
    });
    $('.btn-size').click(function(){
      var this_val = $(this).html();
      $("#product-size").val(this_val);
      $(".btn-size").removeClass('btn-secondary');
      $(".btn-size").addClass('btn-success');
      $(this).removeClass('btn-success');
      $(this).addClass('btn-secondary');
      return false;
    });
    // End roduct detail

});

$(document).ready(function() {
  // Close modal when clicking outside of it
  $(document).on('click', function(e) {
    if ($(e.target).hasClass('modal')) {
      $('#myModal').modal('hide');
    }
  });
});

function attachModalToButton(buttonId, modalId) {
  const button = document.getElementById(buttonId);

  if (button !== null) {
      button.addEventListener('click', function () {
          var myModal = new bootstrap.Modal(document.getElementById(modalId));
          if (buttonId === 'confirmDelete') {
              document.getElementById(buttonId).value = this.value;
          }
          myModal.show();
      });
  }
}

attachModalToButton('openFoodList', 'createFoodListingModal');
attachModalToButton('openSustainableList', 'createSustainableListingModal');