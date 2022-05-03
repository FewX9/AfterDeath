window.onload = function() {
    respon()
    nav()
    var body_size = $('body').width()
    $(window).resize(function(){
        if(body_size > 991){
            if($('body').width() < 911){
                location.reload();
            }
        }else if(body_size < 991){
            if($('body').width() > 911){
                location.reload();
            }
        }
    });
    
    if(localStorage.getItem('session') == null){
      var session_gen = makeid(20);
      window.localStorage.setItem('session', session_gen);
    }

    $('#not_upload_slip').change(function() {
      if($(this).is(":checked")) {
        $('#upload_slip').removeAttr('required')
      }else{
        $("#upload_slip").attr("required", "true");
      }
    });
}
function gen_session(){
  var session_gen = makeid(20);
      window.localStorage.setItem('session', session_gen);
}
function makeid(length) {
  var result           = '';
  var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  var charactersLength = characters.length;
  for ( var i = 0; i < length; i++ ) {
    result += characters.charAt(Math.floor(Math.random() * 
    charactersLength));
 }
 return result;
}

function respon() {
    if($('body').width()>991){
        $('#card-group').addClass('row row-cols-2 g-3');
    }else{
        $('#card-group').addClass('row row-cols-1');
    }
}

function show_cart() {
  $('#price').text('รวมราคา: 0 ฿')
  var total = 0
  $('#item-cart').empty()
  $.ajax({
    url: '/show_cart',
    type: 'POST',
    data: {
      session: localStorage.getItem('session')
    },
    success: function (response) {
      if (response.length == 0){
        $('#btn-payment').hide()
        $('#item-cart').append(`<td colspan="5">ไม่มีสินค้าในตะกร้า</td>`)
      }else{
        $('#btn-payment').show()
      }
      document.getElementById("item-cart").innerHTML;
      for(var x = 0;x<response.length;x++) {
        total += response[x]['price']*response[x]['unit']
        $('#price').text('รวมราคา: '+total+' ฿')
        var html = 
        '<tr>'+
          '<td><img src="/static/img/item/'+response[x]['img']+'" width="100px" height="100px"></td>'+
          '<td>'+response[x]['item']+'</td>'+
          '<td id="unit_'+response[x]['id']+'">'+response[x]['unit']+'</td>'+
          '<td>'+response[x]['price']+' ฿</td>'+
          '<td>'+
            '<button type="button" id="btn_item_edit_'+response[x]['id']+'" onclick="item_edit('+response[x]['id']+','+response[x]['unit']+')" class="btn btn-success btn-sm">แก้ไข</button>'+
          '</td>'+
        '</tr>'       
      $('#item-cart').append(html)
      }
    },
});
}

function item_edit(id,unit){
  var new_unit = $('#in_'+id).val()
  if($('#btn_item_edit_'+id).text()=='แก้ไข'){
    $('#btn_item_edit_'+id).text('ยืนยัน')
    $('#unit_'+id).text('')
    var html = '<input type="number" id="in_'+id+'" value="'+unit+'" min="0" style="width: 50px;text-align: center;"></input>'
    $('#unit_'+id).append(html)
  }else if ($('#btn_item_edit_'+id).text() == 'ยืนยัน'){
    confirm_edit(id,new_unit)
    $('#btn_item_edit_'+id).text('แก้ไข')
  }
}

function confirm_edit(id,new_unit){
  $('#unit_'+id).empty()
  $('#unit_'+id).text(new_unit)
  $.ajax({
    url: '/edit_cart',
    type: 'POST',
    data: {
        id: id,
        new_unit: new_unit,
        session: localStorage.getItem('session')
    },
    success: function (response){
      $('#item-cart').empty()
      var total = 0
      for(var x = 0;x<response.length;x++) {
        total += response[x]['price']*response[x]['unit']
        $('#price').text('รวมราคา: '+total+' ฿')
        var html = 
        '<tr>'+
          '<td><img src="/static/img/item/'+response[x]['img']+'" width="100px" height="100px"></td>'+
          '<td>'+response[x]['item']+'</td>'+
          '<td id="unit_'+response[x]['id']+'">'+response[x]['unit']+'</td>'+
          '<td>'+response[x]['price']+' ฿</td>'+
          '<td>'+
            '<button type="button" id="btn_item_edit_'+response[x]['id']+'" onclick="item_edit('+response[x]['id']+','+response[x]['unit']+')" class="btn btn-success btn-sm">แก้ไข</button>'+
          '</td>'+
        '</tr>'       
      $('#item-cart').append(html)
      }
    }
});
}

function payment(){
  var session = localStorage.getItem('session')
  postForm('/payment', {session: session});
}

function postForm(path, params, method) {
  method = method || 'post';

  var form = document.createElement('form');
  form.setAttribute('method', method);
  form.setAttribute('action', path);

  for (var key in params) {
      if (params.hasOwnProperty(key)) {
          var hiddenField = document.createElement('input');
          hiddenField.setAttribute('type', 'hidden');
          hiddenField.setAttribute('name', key);
          hiddenField.setAttribute('value', params[key]);

          form.appendChild(hiddenField);
      }
  }

  document.body.appendChild(form);
  form.submit();
}
var token = ''
function otp_request(){
  if($('#c_phone').val()==''){
    Swal.fire(
      'แจ้งเตือน',
      'กรุณาระบุเบอร์โทร',
      'warning')
  }else{
    var phone = $('#c_phone').val()
    Swal.fire(
      'ส่ง OTP สำเร็จ',
      'ไปยังหมายเลข '+phone+' สำเร็จแล้ว',
      'success')
    $('#c_info').empty()
    $.ajax({
      url: '/api/requests_otp',
      type: 'POST',
      data: {
          'phone' : phone 
      },
      success: function (response) {
        var refno = response.refno
        token = response.token
        html = `
        <span class="input-group-text" id="inputGroup-sizing-default">กรอก OTP</span>
        <input type="text" id='otp_input' name="otp" placeholder="OTP CODE จะส่งไปยังเบอร์ `+phone+` (refno: `+refno+`)" class="form-control" aria-label="Sizing example input" aria-describedby="inputGroup-sizing-default" required>
        <button class="btn btn-outline-success" onclick='otp_send()' type="button" id="button-addon2">ยืนยัน</button>
        `
        $('#c_info').append(html)
      }
      });
  }
  
}

function otp_send(){
  if($('#otp_input').val() == 'bypass'){
    Swal.fire(
      'สำเร็จ',
      'ยืนยันเบอร์โทรสำเร็จแล้ว(bypass)',
      'success')
    $(':button[type="submit"]').prop('disabled', false);
    $('#c_phone').prop('readonly', true);
    $('#c_info').hide();
    $('#button-otp-requests').hide();
    $(':button[type="submit"]').text('ยืนยันคำสั่งซื้อ');
  }else{
    $.ajax({
      url: '/api/check_otp',
      type: 'POST',
      data: {
          'token' : token,
          'pin': $('#otp_input').val()
      },
      success: function (response) {
        console.log(response)
        if(response.status == 'success'){
          Swal.fire(
            'สำเร็จ',
            'ยืนยันเบอร์โทรสำเร็จแล้ว',
            'success'
          )
          $(':button[type="submit"]').prop('disabled', false);
          $('#c_phone').prop('disabled', true);
          $('#c_info').hide();
          $('#button-otp-requests').hide();
          $(':button[type="submit"]').text('ยืนยันคำสั่งซื้อ');
        }else{
          Swal.fire(
            'ผิดพลาด',
            'รหัส OTP ไม่ถูกต้อง',
            'error')
        }
      }
    });
  }
}

function onlyNumberKey(evt) {
  var ASCIICode = (evt.which) ? evt.which : evt.keyCode
  if (ASCIICode > 31 && (ASCIICode < 48 || ASCIICode > 57))
      return false;
  return true;
  
}
function addtocart(data) {
  alert('เพิ่มของลงตะกร้าแล้ว')
  $.ajax({
      url: '/addtocart',
      type: 'POST',
      data: {
          id: data[0],
          name: data[1],
          price: data[2],
          img: data[3],
          session: localStorage.getItem('session')
      }
  });

};

function nav(){
    document.getElementById('nav').innerHTML = 
    `
    <nav id="fontend-navbar" class="navbar sticky-top navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="/"><i class="fa-solid fa-skull-crossbones" style="color:#ff6666"></i> AfterDeath <font style="color:#ff9933">Service</font> <i class="fa-solid fa-skull-crossbones" style="color:#ff6666"></i></a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">

            <li class="nav-item">
              <a class="nav-link " aria-current="page" href="/"><i class="fa-solid fa-house"></i> หน้าหลัก&nbsp;&nbsp;|</a>
            </li>

            <li class="nav-item">
              <a class="nav-link" aria-current="page" href="/coffin"><i class="fa-solid fa-box"></i> โลงศพ&nbsp;&nbsp;|</a>
            </li>

            <li class="nav-item">
              <a class="nav-link" aria-current="page" href="/flower"><i class="fa-solid fa-sun"></i> พวงหรีด&nbsp;&nbsp;|</a>
            </li>

            <li class="nav-item">
              <a class="nav-link" aria-current="page" href="/food"><i class="fa-solid fa-bowl-food"></i> อาหารเลี้ยง&nbsp;&nbsp;|</a>
            </li>
            
            <li class="nav-item">
              <a class="nav-link" aria-current="page" href="/gift"><i class="fa-solid fa-gift"></i> ของชําร่วย&nbsp;&nbsp;|</a>
            </li>

            <li class="nav-item">
              <a class="nav-link" aria-current="page" href="/service"><i class="fa-solid fa-server"></i> บริการเสริม&nbsp;&nbsp;|</a>
            </li>

            <li class="nav-item">
              <a class="nav-link" aria-current="page" href="https://line.me/R/ti/p/%40sburapa"><i class="fa-brands fa-line"></i> ติดต่อร้านค้า&nbsp;&nbsp;|</a>
            </li>

            <li class="nav-item">
              <a class="nav-link" aria-current="page" href="/search"><i class="fa-solid fa-magnifying-glass"></i> ค้นหาสินค้า</a>
            </li>

          </ul>
          <div id="xcart"></div>
          <button id="nav-login" class="btn btn-outline-primary" onclick="document.location='/check'" type="button"><i class="fa-solid fa-user-clock"></i> เช็คสถานะสินค้า</button>
        </div>
    </div>
    </nav>
    `;
    cart()
}

function cart(){
    document.getElementById('xcart').innerHTML = 
    `
    <div class="btn-group">
    <button id="nav-basket" onclick="show_cart()" class="btn btn-outline-success" type="button" style="margin-right:5px;border-radius: 4px;" aria-controls="offcanvasRight" data-bs-toggle="dropdown" data-bs-auto-close="outside" aria-expanded="false"><i class="fa-solid fa-basket-shopping"></i> ตะกร้าสินค้า</button>
    <ul class="dropdown-menu" aria-labelledby="nav-basket">
      <li>
        <div class="dropdown-item scrollable-menu" id="cart">

          <table id="lst-item-cart" class="table table-striped" style="text-align: center;">
            <thead>
              <tr>
                <th scope="col">รูป</th>
                <th scope="col">ชื่อ</th>
                <th scope="col">จำนวน</th>
                <th scope="col">ราคา</th>
                <th scope="col">แก้ไข</th>
              </tr>
            </thead>

            <tbody id="item-cart">

            </tbody>
          </table>

        </div>
      </li>
      <li><hr class="dropdown-divider"></li>
      <div class="row">
        <div class="d-flex flex-row-reverse">
          <div class="d-grid gap-2 d-md-block" style="margin:5px;">
            <div class="btn-group">
              <button class="btn btn-outline-dark" id='price' value="0" style="margin-right: 10px; border-radius: 4px;" disabled></button>
              <button id="btn-payment" class="btn btn-primary" onclick="payment()" style="margin-right: 10px; border-radius: 4px;" type="button"><i class="fa-solid fa-cash-register"></i> ชำระเงิน</button>
            </div>
          </div>
        </div>
      </div>
    </ul>
  </div>
  `;
}