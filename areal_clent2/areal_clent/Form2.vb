Imports System.Net
Imports System.IO
Imports System.ComponentModel
Imports System.Reflection

Public Class Form2
    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
        If txtAddr.Text <> "" Then
            Timer1.Enabled = True
        End If
    End Sub

    Private Function GetMyDir() As String
        Dim s As String
        s = System.IO.Path.GetDirectoryName(Me.GetType().Assembly.Location)
        Return s
    End Function

    Private Sub Timer1_Tick(sender As Object, e As EventArgs) Handles Timer1.Tick
        ' Create a request for the URL. 
        Dim request As WebRequest
        Dim response As WebResponse
        Dim dataStream As Stream
        Dim reader As StreamReader
        Dim responseFromServer As String
        Dim i As Integer
        Dim j As Integer
        Dim k As Integer
        Dim l As Integer
        Dim s As String
#Region "read"
        Try
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


            Try
                i = Integer.Parse(responseFromServer)
            Catch ex As Exception
                i = 0
            End Try

        Catch ex As Exception

        End Try


        Try
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
                j = Integer.Parse(responseFromServer)
            Catch ex As Exception
                j = 0
            End Try

        Catch ex As Exception

        End Try

        Try
            request = WebRequest.Create("http://" & txtAddr.Text & "/readx?ireg=2")
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
                k = Integer.Parse(responseFromServer)
            Catch ex As Exception
                k = 0
            End Try

        Catch ex As Exception

        End Try


        Try
            request = WebRequest.Create("http://" & txtAddr.Text & "/readx?ireg=3")
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
                l = Integer.Parse(responseFromServer)
            Catch ex As Exception
                l = 0
            End Try

        Catch ex As Exception

        End Try
#End Region

        Dim t As Integer
        Dim m As Boolean = False



        If (k And 1) = 1 Then
            lblPower.BackColor = Color.Red
        Else
            lblPower.BackColor = Color.Green
        End If

        If (k And 2) = 2 Then
            lblPop.BackColor = Color.Red
        Else
            lblPop.BackColor = Color.Green
        End If

        s = ""
        t = 0
        If (i And 1) = 1 Then
            t = 1
            s = "сухой ход"
        End If

        If (i And 2) = 2 Then
            t = 2
            s = "1 уровень"
        End If

        If (i And 4) = 4 Then
            t = 3
            s = "2 уровень"
        End If
        If (i And 8) = 8 Then
            s = "3 уровень"
            t = 4
        End If
        If (i And 16) = 16 Then
            s = "аварийный уровень"
            t = 5
        End If
        picTank.Image = Image.FromFile(GetMyDir() & "\images\tank_" & t.ToString & ".png")
        lblT.Text = s

        m = True
        t = 0
        s = ""
        If (i And 128) = 128 Then
            t = 3
            s = "готовность"
        End If

        If (i And 256) = 256 Then
            t = 1
            s = "работа"
        End If

        If (k And 16) = 16 Then
            t = 2
            s = "авария"
        End If

        If (i And 512) = 512 Then
            m = False
            s = "авт. " & s
        Else


            s = "руч. " & s
        End If

        If m Then
            picPump1.Image = Image.FromFile(GetMyDir() & "\images\manPump_" & t.ToString & ".png")
        Else
            picPump1.Image = Image.FromFile(GetMyDir() & "\images\pump_" & t.ToString & ".png")
        End If
        lblP1.Text = s



        m = True
        t = 0
        s = ""
        If (i And 1024) = 1024 Then
            t = 3
            s = "готовность"
        End If

        If (i And 2048) = 2048 Then
            t = 1
            s = "работа"
        End If

        If (k And 64) = 64 Then
            t = 2
            s = "авария"
        End If


        If (j And 1) = 1 Then
            m = False
            s = "авт. " & s
        Else


            s = "руч. " & s
        End If

        If m Then
            picPump2.Image = Image.FromFile(GetMyDir() & "\images\manPump_" & t.ToString & ".png")
        Else
            picPump2.Image = Image.FromFile(GetMyDir() & "\images\pump_" & t.ToString & ".png")
        End If
        lblP2.Text = s


        m = True
        t = 0
        s = ""
        If (j And 2) = 2 Then
            t = 3
            s = "готовность"
        End If

        If (j And 4) = 4 Then
            t = 1
            s = "работа"
        End If

        If (l And 1) = 1 Then
            t = 2
            s = "авария"
        End If

        If (j And 8) = 8 Then
            m = False
            s = "авт. " & s
        Else


            s = "руч. " & s
        End If

        If m Then
            picPump3.Image = Image.FromFile(GetMyDir() & "\images\manPump_" & t.ToString & ".png")
        Else
            picPump3.Image = Image.FromFile(GetMyDir() & "\images\pump_" & t.ToString & ".png")
        End If
        lblP3.Text = s


        'request = WebRequest.Create("http://" & txtAddr.Text & "/readx?ireg=1")
        '' If required by the server, set the credentials.
        'request.Credentials = CredentialCache.DefaultCredentials
        '' Get the response.
        'response = request.GetResponse()

        'dataStream = response.GetResponseStream()
        '' Open the stream using a StreamReader for easy access.
        'reader = New StreamReader(dataStream)
        '' Read the content.
        'responseFromServer = reader.ReadToEnd()

        'reader.Close()
        'response.Close()

        'Try
        '    i = Integer.Parse(responseFromServer)
        'Catch ex As Exception
        '    i = 0
        'End Try


        'If (i And 8) = 8 Then
        '    A1.BackColor = Color.Red
        'Else
        '    A1.BackColor = Color.LightGray
        'End If

        'If (i And 4) = 4 Then
        '    W1.BackColor = Color.Green
        'Else
        '    W1.BackColor = Color.LightGray
        'End If
    End Sub

    Private Sub Form2_Closing(sender As Object, e As CancelEventArgs) Handles Me.Closing
        Timer1.Enabled = False
    End Sub
End Class