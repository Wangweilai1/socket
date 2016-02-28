// server.cpp : Defines the entry point for the console application.
//
#include "stdafx.h"
#include <winsock2.h>
#include <Windows.h>
#include<conio.h>

#pragma comment (lib, "ws2_32.lib")   //加载 ws2_32.dll

int g_postion = 1;
CRITICAL_SECTION gcc;

void gotoxy(int x, int y);
COORD get_xy();
void ClearScreen(void);
void ClearScreen1(void);
DWORD WINAPI  sendCustmer(LPVOID);
DWORD WINAPI  displayServer(LPVOID);


int main()
{
    system("cls");
    HANDLE    hThread1 = NULL;
    HANDLE    hThread2 = NULL;
    HANDLE hOut;
    hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    WORD att = FOREGROUND_RED|FOREGROUND_GREEN|FOREGROUND_INTENSITY|BACKGROUND_BLUE;
    SetConsoleTextAttribute(hOut, att);
    SMALL_RECT rc = {0, 0, 80, 25};
    SetConsoleWindowInfo(hOut, true,&rc);
    SetConsoleTitle(L"The Chat Tools ");
    ClearScreen();
    InitializeCriticalSection(&gcc);
    hThread1 = CreateThread(NULL, NULL, displayServer, NULL, NULL, NULL);
    hThread2 = CreateThread(NULL, NULL, sendCustmer, NULL, NULL, NULL);
    HANDLE    tHandle[] = {hThread1, hThread2};
    WaitForMultipleObjects(2, tHandle, true, INFINITE);
    DeleteCriticalSection(&gcc);

    WSACleanup();
    CloseHandle(hThread1);
    CloseHandle(hThread2);

}



DWORD WINAPI sendCustmer(LPVOID lpParameter)
{
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2, 2), &wsaData);

    //向服务器发起请求
    sockaddr_in sockAddr;
    memset(&sockAddr, 0, sizeof(sockAddr));  //每个字节都用0填充
    sockAddr.sin_family = PF_INET;
    sockAddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    //sockAddr.sin_addr.s_addr = htonl(INADDR_ANY);
    sockAddr.sin_port = htons(1234);
    char SendBuffer[MAXBYTE];

    while (1)
    {
        SOCKET sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
        do 
        {
            if (0 == connect(sock, (SOCKADDR*)&sockAddr, sizeof(SOCKADDR)))
            {
                break;
            }
        } while (true);
        memset(SendBuffer, 0, MAXBYTE);

        gotoxy(0, 21);
        ClearScreen1();
#if 0
        for (int j = 0; j < 100; ++j)
        {
            printf_s(" ");
        }
#endif
        do 
        {
            gotoxy(0, 21);
            gets_s (SendBuffer);
        } while ( 0 == strlen(SendBuffer) );
        gotoxy(0, g_postion);
        if (g_postion < 20)
        {
            ++g_postion;
        }
        else
        {
            g_postion = 1;
            gotoxy(0, g_postion);
            ++g_postion;
            ClearScreen();
            //system("cls");
        }
        printf_s("I'm: %s\n", SendBuffer);
        send(sock, SendBuffer, strlen(SendBuffer) + sizeof(char), NULL);
        shutdown(sock, SD_SEND);
        closesocket(sock);
    }
    return 0;
}


DWORD WINAPI displayServer(LPVOID lpParameter)
{
    WSADATA wsaData;
    WSAStartup( MAKEWORD(2, 2), &wsaData);

    //创建套接字
    SOCKET servSock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);

    //绑定套接字
    sockaddr_in  sockAddr;
    memset(&sockAddr, 0, sizeof(sockAddr));                  //每个字节都用0填充
    sockAddr.sin_family = PF_INET;                           //使用IPv4地址
    sockAddr.sin_addr.s_addr = htonl(INADDR_ANY);            //自动获取IP地址
    sockAddr.sin_port = htons(4321);                         //端口
    bind(servSock, (SOCKADDR*)&sockAddr, sizeof(SOCKADDR));

    //进入监听状态
    listen(servSock, 20);

    //接收客户端请求
    SOCKADDR clntAddr;
    int nSize = sizeof(SOCKADDR);
    SOCKET clntSock;
    char RecvBuffer[MAXBYTE];
    COORD old_postion = {0, 0};
    while (1)
    {
        clntSock = accept(servSock, (SOCKADDR*)&clntAddr, &nSize);
        memset(RecvBuffer, 0, MAXBYTE);
        do 
        {
            recv(clntSock, RecvBuffer, MAXBYTE, NULL);
        } while (0 == strlen(RecvBuffer));
        old_postion = get_xy();

        if (g_postion < 20)
        {
            gotoxy(0, g_postion++);
        }
        else
        {
            g_postion = 1;
            gotoxy(0, g_postion);
            ++g_postion;
            ClearScreen();
            //system("cls");
        }
        printf_s("You: %s\n", RecvBuffer);
        gotoxy(old_postion.X, old_postion.Y);
    }

    //关闭套接字
    closesocket(clntSock);
    closesocket(servSock);

    //终止 DLL 的使用
    WSACleanup();
    system("pause");
    return 0;
}

void gotoxy(int x,int y)
{
    HANDLE hOutput;
    COORD loc;
    loc.X = x;
    loc.Y = y;
    hOutput= GetStdHandle(STD_OUTPUT_HANDLE);
    SetConsoleCursorPosition(hOutput, loc);
}

COORD get_xy()
{
    COORD postion = {0, 0};
    CONSOLE_SCREEN_BUFFER_INFO csbi;
    HANDLE hStdOut = GetStdHandle(STD_OUTPUT_HANDLE);
    GetConsoleScreenBufferInfo( hStdOut, &csbi );
    postion = csbi.dwCursorPosition;
    return postion;
}

void ClearScreen(void)
{
    HANDLE hOut;
    DWORD written;
    hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    CONSOLE_SCREEN_BUFFER_INFO bInfo;
    GetConsoleScreenBufferInfo( hOut, &bInfo ); 
    COORD home = {0, 0};
    WORD att = bInfo.wAttributes;
    unsigned long size = bInfo.dwSize.X * 21;
    FillConsoleOutputAttribute(hOut, att, size, home, &written);
    FillConsoleOutputCharacter(hOut, ' ', size, home, &written);
}
void ClearScreen1(void)
{
    HANDLE hOut;
    DWORD written;
    hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    CONSOLE_SCREEN_BUFFER_INFO bInfo;
    GetConsoleScreenBufferInfo( hOut, &bInfo ); 
    COORD home = {0, 21};
    WORD att = bInfo.wAttributes;
    unsigned long size = bInfo.dwSize.X  * (bInfo.dwSize.Y - 21);
    FillConsoleOutputAttribute(hOut, att, size, home, &written);
    FillConsoleOutputCharacter(hOut, ' ', size, home, &written);
}
