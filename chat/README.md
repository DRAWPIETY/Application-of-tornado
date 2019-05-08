说明：
  关于static/chat.js的ws='localhost:8888/....'的注意事项
  该程序在使用过程中未修改该语句，则在本机输入网址localhost:8888或127.0.0.1，能够连接websocket,
  然而，在同一局域网连接的除本机外的设备登陆该网页，需要将localhost修改为后端运行的机器的ipv4地址，并且其他无法连接websocket。
  想要在同意局域网不同的设备间连接websocket，需要把static/chat.js的ws='localhost:8888/....'中的localhost改为ipv4地址，
  本机再输入localhost:8888可以进入登陆页面，但无法连接websocket，本机要想连接，也只能输入“ipv4地址：8888”
