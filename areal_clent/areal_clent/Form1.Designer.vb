<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class Form1
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
        Me.L1 = New System.Windows.Forms.Label()
        Me.L2 = New System.Windows.Forms.Label()
        Me.L3 = New System.Windows.Forms.Label()
        Me.W1 = New System.Windows.Forms.Label()
        Me.A1 = New System.Windows.Forms.Label()
        Me.cmdStop = New System.Windows.Forms.Button()
        Me.txtAddr = New System.Windows.Forms.TextBox()
        Me.Label5 = New System.Windows.Forms.Label()
        Me.Timer1 = New System.Windows.Forms.Timer(Me.components)
        Me.Button1 = New System.Windows.Forms.Button()
        Me.Button2 = New System.Windows.Forms.Button()
        Me.SuspendLayout()
        '
        'L1
        '
        Me.L1.BackColor = System.Drawing.Color.Yellow
        Me.L1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
        Me.L1.Location = New System.Drawing.Point(23, 72)
        Me.L1.Name = "L1"
        Me.L1.Size = New System.Drawing.Size(73, 47)
        Me.L1.TabIndex = 0
        Me.L1.Text = "Датчик 1"
        Me.L1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        '
        'L2
        '
        Me.L2.BackColor = System.Drawing.Color.Yellow
        Me.L2.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
        Me.L2.Location = New System.Drawing.Point(23, 161)
        Me.L2.Name = "L2"
        Me.L2.Size = New System.Drawing.Size(73, 47)
        Me.L2.TabIndex = 1
        Me.L2.Text = "Датчик 2"
        Me.L2.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        '
        'L3
        '
        Me.L3.BackColor = System.Drawing.Color.Yellow
        Me.L3.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
        Me.L3.Location = New System.Drawing.Point(23, 249)
        Me.L3.Name = "L3"
        Me.L3.Size = New System.Drawing.Size(73, 47)
        Me.L3.TabIndex = 2
        Me.L3.Text = "Датчик 3"
        Me.L3.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        '
        'W1
        '
        Me.W1.BackColor = System.Drawing.Color.Yellow
        Me.W1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
        Me.W1.Location = New System.Drawing.Point(195, 72)
        Me.W1.Name = "W1"
        Me.W1.Size = New System.Drawing.Size(73, 47)
        Me.W1.TabIndex = 3
        Me.W1.Text = "Работа"
        Me.W1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        '
        'A1
        '
        Me.A1.BackColor = System.Drawing.Color.Yellow
        Me.A1.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle
        Me.A1.Location = New System.Drawing.Point(365, 72)
        Me.A1.Name = "A1"
        Me.A1.Size = New System.Drawing.Size(73, 47)
        Me.A1.TabIndex = 4
        Me.A1.Text = "Авария"
        Me.A1.TextAlign = System.Drawing.ContentAlignment.MiddleCenter
        '
        'cmdStop
        '
        Me.cmdStop.Font = New System.Drawing.Font("Microsoft Sans Serif", 24.0!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(204, Byte))
        Me.cmdStop.ForeColor = System.Drawing.Color.Red
        Me.cmdStop.Location = New System.Drawing.Point(195, 149)
        Me.cmdStop.Name = "cmdStop"
        Me.cmdStop.Size = New System.Drawing.Size(243, 79)
        Me.cmdStop.TabIndex = 5
        Me.cmdStop.Text = "Останов"
        Me.cmdStop.UseVisualStyleBackColor = True
        '
        'txtAddr
        '
        Me.txtAddr.Location = New System.Drawing.Point(131, 8)
        Me.txtAddr.Name = "txtAddr"
        Me.txtAddr.Size = New System.Drawing.Size(217, 20)
        Me.txtAddr.TabIndex = 6
        Me.txtAddr.Text = "192.168.3.120"
        '
        'Label5
        '
        Me.Label5.AutoSize = True
        Me.Label5.Location = New System.Drawing.Point(12, 11)
        Me.Label5.Name = "Label5"
        Me.Label5.Size = New System.Drawing.Size(81, 13)
        Me.Label5.TabIndex = 7
        Me.Label5.Text = "УСПД. АРЕАЛ"
        '
        'Timer1
        '
        Me.Timer1.Interval = 1000
        '
        'Button1
        '
        Me.Button1.Location = New System.Drawing.Point(362, 8)
        Me.Button1.Name = "Button1"
        Me.Button1.Size = New System.Drawing.Size(75, 20)
        Me.Button1.TabIndex = 8
        Me.Button1.Text = "включить"
        Me.Button1.UseVisualStyleBackColor = True
        '
        'Button2
        '
        Me.Button2.Font = New System.Drawing.Font("Microsoft Sans Serif", 24.0!, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, CType(204, Byte))
        Me.Button2.ForeColor = System.Drawing.Color.Lime
        Me.Button2.Location = New System.Drawing.Point(194, 234)
        Me.Button2.Name = "Button2"
        Me.Button2.Size = New System.Drawing.Size(243, 79)
        Me.Button2.TabIndex = 9
        Me.Button2.Text = "Пуск"
        Me.Button2.UseVisualStyleBackColor = True
        '
        'Form1
        '
        Me.AutoScaleDimensions = New System.Drawing.SizeF(6.0!, 13.0!)
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.ClientSize = New System.Drawing.Size(463, 348)
        Me.Controls.Add(Me.Button2)
        Me.Controls.Add(Me.Button1)
        Me.Controls.Add(Me.Label5)
        Me.Controls.Add(Me.txtAddr)
        Me.Controls.Add(Me.cmdStop)
        Me.Controls.Add(Me.A1)
        Me.Controls.Add(Me.W1)
        Me.Controls.Add(Me.L3)
        Me.Controls.Add(Me.L2)
        Me.Controls.Add(Me.L1)
        Me.Name = "Form1"
        Me.Text = "УСПД АРЕАЛ ТЕСТ"
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub

    Friend WithEvents L1 As Label
    Friend WithEvents L2 As Label
    Friend WithEvents L3 As Label
    Friend WithEvents W1 As Label
    Friend WithEvents A1 As Label
    Friend WithEvents cmdStop As Button
    Friend WithEvents txtAddr As TextBox
    Friend WithEvents Label5 As Label
    Friend WithEvents Timer1 As Timer
    Friend WithEvents Button1 As Button
    Friend WithEvents Button2 As Button
End Class
