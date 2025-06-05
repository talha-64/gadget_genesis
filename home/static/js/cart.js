var add_cart_btns = document.getElementsByClassName('add_cart_btn')


Array.from(add_cart_btns).forEach(element => {
  element.addEventListener('click', function(e){
    e.preventDefault();
    var prod_id = this.dataset.product
    window.location.href = `/cart/?product_id=${prod_id}`;
  })
});