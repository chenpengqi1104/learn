function validateForm()
{
  var x=document.forms["f1"]["username"].value;
  if (x==null || x=="")
  {
    alert("name须填写");
    return false;
  }

  var y=document.forms["f1"]["password"].value;
  var pwd2 = document.forms["f1"]["password1"].value;
  if (y==null || y=="")
  {
    alert("输入错误");
    return false;
  }
  if (y!=pwd2){
    alert("密码不一致");
    return false;
  }





}// JavaScript Document