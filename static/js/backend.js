window.onload = function() {
  respon()
  nav()
}
function respon() {
  if($('body').width()>991){
      $('#card-group').addClass('row row-cols-2 g-3');
  }else{
      $('#card-group').addClass('row row-cols-1');
  }
}
function edit_report(date,income,payment){
  $("#date-in").val(date);
  $("#income-in").val(income);
  $("#payment-in").val(payment);
  $("#title").text('แก้ไขข้อมูล วันที่: '+date);
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
function check_role(){
    if(Cookies.get("role") == 'admin'){
        var html = `
        <ul class="navbar-nav">
                <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDarkDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                <i class="fa-solid fa-users"></i></i> จัดการข้อมูลพนักงาน
                </a>
                <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="navbarDarkDropdownMenuLink">
                <a class="nav-link " aria-current="page" href="/account"><i class="fa-solid fa-user"></i> แก้ไขบัญชีพนักงาน</a>
                <a class="nav-link " aria-current="page" href="/add_account"><i class="fa-solid fa-user-plus"></i> เพิ่มบัญชีพนักงาน</a>
                </ul>
                </li>
              </ul>
        `
        $('#admin_menu').append(html)
    }
}
function x_confirm_order(id,name,phone){
  $.ajax({
    url: '/backend/confirm_order',
    type: 'POST',
    data: {
        id: id,
        name: name,
        phone: phone,
    },
    success: function (response) {
      if (response == 'success'){
        window.open("/backend/confirm_order/success");
      }
    }
});
}
function confirm_order(order_id){
  var html = 
  `<div class="modal fade" id="order_connnnn" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true" role="dialog">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-body">
                      <div class="thank-you-pop">
                      
                      <h1><i class="fa-solid fa-user"></i> ข้อมูลผู้จัดส่ง</h1>

                      <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1">ชื่อผู้ส่ง</span>
                        <input type="text" class="form-control" id="s_name" placeholder="ชื่อผู้จัดส่ง" aria-label="Username" aria-describedby="basic-addon1" required>
                      </div>

                      <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1">เบอร์โทรผู้ส่ง</span>
                        <input type="text" class="form-control" id="s_phone" placeholder="เบอร์โทรผู้จัดส่ง" aria-label="Username" aria-describedby="basic-addon1" required>
                      </div>

                      <div class="d-grid gap-2 d-md-block">
                        <button onclick="x_confirm_order(`+order_id+`,$('#s_name').val(),$('#s_phone').val())" class="btn btn-success" type="button" style="width: 45%;">ยืนยัน</button>
                        <button onclick="$('#order_connnnn').modal('hide')" class="btn btn-danger" type="button" style="width: 45%;">ยกเลิก</button>
                      </div>

                      </div>     
                    </div>
                </div>
            </div>
        </div>`
  $('body').append(html)
  $('#order_connnnn').modal('show');
}
function nav(){
    document.getElementById('nav').innerHTML = 
    `
    <nav id="fontend-navbar" class="navbar sticky-top navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="/">After Death</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">

            <li class="nav-item">
              <ul class="navbar-nav">
                <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDarkDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                <i class="fa-solid fa-bars-progress"></i> แก้ไขรายการสินค้า
                </a>
                <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="navbarDarkDropdownMenuLink">
                    <li><a class="dropdown-item" href="/backend/edit_coffin"><i class="fa-solid fa-box"></i> แก้ไขรายการโลงศพ</a></li>
                    <li><a class="dropdown-item" href="/backend/edit_food"><i class="fa-solid fa-bowl-food"></i> แก้ไขรายการอาหาร</a></li>
                    <li><a class="dropdown-item" href="/backend/edit_gift"><i class="fa-solid fa-gift"></i> แก้ไขรายการของชําร่วย</a></li>
                    <li><a class="dropdown-item" href="/backend/edit_flower"><i class="fa-solid fa-sun"></i> แก้ไขรายการพวงหรีด</a></li>
                </ul>
                </li>
              </ul>
            </li>

            <li class="nav-item">
              <a class="nav-link " aria-current="page" href="/backend/add_item"><i class="fa-solid fa-plus"></i> เพิ่มรายการสินค้า</a>
            </li>

            <li class="nav-item">
              <a class="nav-link " aria-current="page" href="/backend/order_list"><i class="fa-solid fa-pen-to-square"></i> จัดการออเดอร์</a>
            </li>
            
            <li class="nav-item">
              <a class="nav-link " aria-current="page" href="/backend/report"><i class="fa-solid fa-chart-column"></i> จัดการรายรับรายจ่าย</a>
            </li>
            </li>
            
            <li class="nav-item" id='admin_menu'>
            </li>

          </ul>
          
            <ul class="navbar-nav">
                <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDarkDropdownMenuLink" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                <img src="/static/img/account/`+Cookies.get("img")+`" class="rounded" id='profile_img'> `+Cookies.get("f_name")+` `+Cookies.get("l_name")+`
                </a>
                <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="navbarDarkDropdownMenuLink">
                    <li><button class="dropdown-item" onclick='logout()'><i class="fa-solid fa-arrow-right-from-bracket"></i> ออกจากระบบ</button></li>
                </ul>
                </li>
            </ul>
            
        </div>
    </div>
    </nav>
    `;
    check_role()
}

function logout(){
  Cookies.remove('f_name')
  Cookies.remove('l_name')
  Cookies.remove('img')
  Cookies.remove('role')
  window.location.href = '/login';
}
function show_cart(session) {
  var total = 0
  $('#item-cart').empty()
  $.ajax({
    url: '/show_cart',
    type: 'POST',
    data: {
      session: session
    },
    success: function (response) {
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
        '</tr>'       
      $('#item-cart').append(html)
      }
    },
});
}
function show_item(session) {
  var html = 
  `<div class="modal fade" id="order_show" role="dialog">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-body">
                      
                    <div class="dropdown-item scrollable-menu" id="cart">

          <table id="lst-item-cart" class="table table-striped" style="text-align: center;">
            <thead>
              <tr>
                <th scope="col">รูป</th>
                <th scope="col">ชื่อ</th>
                <th scope="col">จำนวน</th>
                <th scope="col">ราคา</th>
              </tr>
            </thead>

            <tbody id="item-cart">

            </tbody>
          </table>

        </div>
                    
                    </div>
                </div>
            </div>
        </div>`
  $('body').append(html)
  $('#order_show').modal('show');
  show_cart(session)
}