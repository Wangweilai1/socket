Enter file contents here#include "stdafx.h"
#include <stdlib.h>
#include <WinSock2.h>
#pragma comment(lib, "ws2_32.lib")  //加载 ws2_32.dll

int main(){
    //初始化DLL
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);

    //创建套接字
    SOCKET sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);

    //向服务器发起请求
    sockaddr_in sockAddr;
    memset(&sockAddr, 0, sizeof(sockAddr));  //每个字节都用0填充
    sockAddr.sin_family = PF_INET;
    sockAddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    sockAddr.sin_port = htons(1234);
    connect(sock, (SOCKADDR*)&sockAddr, sizeof(SOCKADDR));
    printf_s("****** Welcome To Use TELE, This Custmer ******\n\n");
    char str[MAXBYTE];
    char szBuffer[MAXBYTE];

    while (1)
    {
        memset(str, 0, MAXBYTE);
        printf_s("Customer: ");
        gets_s (str);
        send(sock, str, strlen(str)+sizeof(char), NULL);
        //接收服务器传回的数据
        memset(szBuffer, 0, MAXBYTE);
        recv(sock, szBuffer, MAXBYTE, NULL);
        //输出接收到的数据
        printf("Server: %s\n", szBuffer);
    }

    //关闭套接字
    closesocket(sock);

    //终止使用 DLL
    WSACleanup();

    system("pause");
    return 0;
}
