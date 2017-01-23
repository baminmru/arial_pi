Imports System.Web
Imports System.Net
Imports System.IO
Imports System.ComponentModel

Public Class Form1
    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
        If txtAddr.Text <> "" Then
            Timer1.Enabled = True
        End If
    End Sub

    Private Sub Timer1_Tick(sender As Object, e As EventArgs) Handles Timer1.Tick
        ' Create a request for the URL. 
        Dim request As WebRequest
        Dim response As WebResponse
        Dim dataStream As Stream
        Dim reader As StreamReader
        Dim responseFromServer As String

        request = WebRequest.Create("http://" & txtAddr.Text & "/readx?ireg=0")
        ' If required by the server, set the credentials.
        request.Credentials = CredentialCache.DefaultCredentials
        ' Get the response.
        response = request.GetResponse()

        dataStream = response.GetResponseStream()
        ' Open the stream using a StreamReader for easy access.
        reader = New StreamReader(dataStream)
        ' Read the content.
        responseFromServer = reader.ReadToEnd()

        reader.Close()
        response.Close()


        Dim i As Integer
        Try
            i = Integer.Parse(responseFromServer)
        Catch ex As Exception
            i = 0
        End Try


        If (i And 1) = 1 Then
            L1.BackColor = Color.Yellow
        Else
            L1.BackColor = Color.LightGray
        End If

        If (i And 2) = 2 Then
            L2.BackColor = Color.Yellow
        Else
            L2.BackColor = Color.LightGray
        End If

        If (i And 4) = 4 Then
            L3.BackColor = Color.Yellow
        Else
            L3.BackColor = Color.LightGray
        End If

        request = WebRequest.Create("http://" & txtAddr.Text & "/readx?ireg=1")
        ' If required by the server, set the credentials.
        request.Credentials = CredentialCache.DefaultCredentials
        ' Get the response.
        response = request.GetResponse()

        dataStream = response.GetResponseStream()
        ' Open the stream using a StreamReader for easy access.
        reader = New StreamReader(dataStream)
        ' Read the content.
        responseFromServer = reader.ReadToEnd()

        reader.Close()
        response.Close()

        Try
            i = Integer.Parse(responseFromServer)
        Catch ex As Exception
            i = 0
        End Try


        If (i And 8) = 8 Then
            A1.BackColor = Color.Red
        Else
            A1.BackColor = Color.LightGray
        End If

        If (i And 4) = 4 Then
            W1.BackColor = Color.Green
        Else
            W1.BackColor = Color.LightGray
        End If

    End Sub

    Private Sub cmdStop_Click(sender As Object, e As EventArgs) Handles cmdStop.Click
        Dim request As WebRequest
        Dim response As WebResponse
        Dim dataStream As Stream
        Dim reader As StreamReader
        Dim responseFromServer As String

        request = WebRequest.Create("http://" & txtAddr.Text & "/set?hreg=2&value=8")
        ' If required by the server, set the credentials.
        request.Credentials = CredentialCache.DefaultCredentials
        ' Get the response.
        response = request.GetResponse()

        dataStream = response.GetResponseStream()
        ' Open the stream using a StreamReader for easy access.
        reader = New StreamReader(dataStream)
        ' Read the content.
        responseFromServer = reader.ReadToEnd()

        reader.Close()
        response.Close()
    End Sub

    Private Sub Button2_Click(sender As Object, e As EventArgs) Handles Button2.Click
        Dim request As WebRequest
        Dim response As WebResponse
        Dim dataStream As Stream
        Dim reader As StreamReader
        Dim responseFromServer As String

        request = WebRequest.Create("http://" & txtAddr.Text & "/set?hreg=2&value=0")
        ' If required by the server, set the credentials.
        request.Credentials = CredentialCache.DefaultCredentials
        ' Get the response.
        response = request.GetResponse()

        dataStream = response.GetResponseStream()
        ' Open the stream using a StreamReader for easy access.
        reader = New StreamReader(dataStream)
        ' Read the content.
        responseFromServer = reader.ReadToEnd()

        reader.Close()
        response.Close()
    End Sub

    Private Sub Form1_Load(sender As Object, e As EventArgs) Handles MyBase.Load

    End Sub

    Private Sub Form1_Closing(sender As Object, e As CancelEventArgs) Handles Me.Closing
        Timer1.Enabled = False
    End Sub
End Class
