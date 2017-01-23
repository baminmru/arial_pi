<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class Form2
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.components = New System.ComponentModel.Container()
        Me.picTank = New System.Windows.Forms.PictureBox()
        Me.Button1 = New System.Windows.Forms.Button()
        Me.Label5 = New System.Windows.Forms.Label()
        Me.txtAddr = New System.Windows.Forms.TextBox()
        Me.Timer1 = New System.Windows.Forms.Timer(Me.components)
        Me.picPump1 = New System.Windows.Forms.PictureBox()
        Me.picPump2 = New System.Windows.Forms.PictureBox()
        Me.picPump3 = New System.Windows.Forms.PictureBox()
        Me.lblP1 = New System.Windows.Forms.Label()
        Me.lblP2 = New System.Windows.Forms.Label()
        Me.lblP3 = New System.Windows.Forms.Label()
        Me.lblT = New System.Windows.Forms.Label()
        Me.lblPop = New System.Windows.Forms.Label()
        Me.lblPower = New System.Windows.Forms.Label()
        CType(Me.picTank, System.ComponentModel.ISupportInitialize).BeginInit()
        CType(Me.picPump1, System.ComponentModel.ISupportInitialize).BeginInit()
        CType(Me.picPump2, System.ComponentModel.ISupportInitialize).BeginInit()
        CType(Me.picPump3, System.ComponentModel.ISupportInitialize).BeginInit()
        Me.SuspendLayout()
        '
        'picTank
        '
        Me.picTank.Image = Global.areal_clent.My.Resources.Resources.tank_0
        Me.picTank.Location = New System.Drawing.Point(223, 57)
        Me.picTank.Name = "picTank"
        Me.picTank.Size = New System.Drawing.Size(103, 202)
        Me.picTank.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
        Me.picTank.TabIndex = 0
        Me.picTank.TabStop = False
        '
        'Button1
        '
        Me.Button1.Location = New System.Drawing.Point(357, 12)
        Me.Button1.Name = "Button1"
        Me.Button1.Size = New System.Drawing.Size(75, 20)
        Me.Button1.TabIndex = 11
        Me.Button1.Text = "включить"
        Me.Button1.UseVisualStyleBackColor = True
        '
        'Label5
        '
        Me.Label5.AutoSize = True
        Me.Label5.Location = New System.Drawing.Point(7, 15)
        Me.Label5.Name = "Label5"
        Me.Label5.Size = New System.Drawing.Size(81, 13)
        Me.Label5.TabIndex = 10
        Me.Label5.Text = "УСПД. АРЕАЛ"
        '
        'txtAddr
        '
        Me.txtAddr.Location = New System.Drawing.Point(126, 12)
        Me.txtAddr.Name = "txtAddr"
        Me.txtAddr.Size = New System.Drawing.Size(217, 20)
        Me.txtAddr.TabIndex = 9
        Me.txtAddr.Text = "192.168.3.120"
        '
        'Timer1
        '
        '
        'picPump1
        '
        Me.picPump1.Location = New System.Drawing.Point(82, 286)
        Me.picPump1.Name = "picPump1"
        Me.picPump1.Size = New System.Drawing.Size(97, 92)
        Me.picPump1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
        Me.picPump1.TabIndex = 12
        Me.picPump1.TabStop = False
        '
        'picPump2
        '
        Me.picPump2.Location = New System.Drawing.Point(223, 286)
        Me.picPump2.Name = "picPump2"
        Me.picPump2.Size = New System.Drawing.Size(97, 92)
        Me.picPump2.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
        Me.picPump2.TabIndex = 13
        Me.picPump2.TabStop = False
        '
        'picPump3
        '
        Me.picPump3.Location = New System.Drawing.Point(370, 286)
        Me.picPump3.Name = "picPump3"
        Me.picPump3.Size = New System.Drawing.Size(97, 92)
        Me.picPump3.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
        Me.picPump3.TabIndex = 14
        Me.picPump3.TabStop = False
        '
        'lblP1
        '
        Me.lblP1.Location = New System.Drawing.Point(75, 382)
        Me.lblP1.Name = "lblP1"
        Me.lblP1.Size = New System.Drawing.Size(113, 19)
        Me.lblP1.TabIndex = 15
        '
        'lblP2
        '
        Me.lblP2.Location = New System.Drawing.Point(213, 382)
        Me.lblP2.Name = "lblP2"
        Me.lblP2.Size = New System.Drawing.Size(113, 19)
        Me.lblP2.TabIndex = 16
        '
        'lblP3
        '
        Me.lblP3.Location = New System.Drawing.Point(367, 382)
        Me.lblP3.Name = "lblP3"
        Me.lblP3.Size = New System.Drawing.Size(113, 19)
        Me.lblP3.TabIndex = 17
        '
        'lblT
        '
        Me.lblT.Location = New System.Drawing.Point(342, 57)
        Me.lblT.Name = "lblT"
        Me.lblT.Size = New System.Drawing.Size(183, 51)
        Me.lblT.TabIndex = 18
        '
        'lblPop
        '
        Me.lblPop.Location = New System.Drawing.Point(370, 137)
        Me.lblPop.Name = "lblPop"
        Me.lblPop.Size = New System.Drawing.Size(97, 92)
        Me.lblPop.TabIndex = 19
        Me.lblPop.Text = "Поплавки"
        Me.lblPop.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        '
        'lblPower
        '
        Me.lblPower.Location = New System.Drawing.Point(79, 137)
        Me.lblPower.Name = "lblPower"
        Me.lblPower.Size = New System.Drawing.Size(97, 92)
        Me.lblPower.TabIndex = 20
        Me.lblPower.Text = "Питание"
        Me.lblPower.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        '
        'Form2
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(590, 404)
        Me.Controls.Add(Me.lblPower)
        Me.Controls.Add(Me.lblPop)
        Me.Controls.Add(Me.lblT)
        Me.Controls.Add(Me.lblP3)
        Me.Controls.Add(Me.lblP2)
        Me.Controls.Add(Me.lblP1)
        Me.Controls.Add(Me.picPump3)
        Me.Controls.Add(Me.picPump2)
        Me.Controls.Add(Me.picPump1)
        Me.Controls.Add(Me.Button1)
        Me.Controls.Add(Me.Label5)
        Me.Controls.Add(Me.txtAddr)
        Me.Controls.Add(Me.picTank)
        Me.Name = "Form2"
        Me.Text = "Form2"
        CType(Me.picTank, System.ComponentModel.ISupportInitialize).EndInit()
        CType(Me.picPump1, System.ComponentModel.ISupportInitialize).EndInit()
        CType(Me.picPump2, System.ComponentModel.ISupportInitialize).EndInit()
        CType(Me.picPump3, System.ComponentModel.ISupportInitialize).EndInit()
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub

    Friend WithEvents picTank As PictureBox
    Friend WithEvents Button1 As Button
    Friend WithEvents Label5 As Label
    Friend WithEvents txtAddr As TextBox
    Friend WithEvents Timer1 As Timer
    Friend WithEvents picPump1 As PictureBox
    Friend WithEvents picPump2 As PictureBox
    Friend WithEvents picPump3 As PictureBox
    Friend WithEvents lblP1 As Label
    Friend WithEvents lblP2 As Label
    Friend WithEvents lblP3 As Label
    Friend WithEvents lblT As Label
    Friend WithEvents lblPop As Label
    Friend WithEvents lblPower As Label
End Class
