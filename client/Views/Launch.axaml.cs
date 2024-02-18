// MobaHinted Copyright (C) 2024 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

using Avalonia.Controls;

namespace client.Views;

public partial class LaunchView : Window
{
    public LaunchView()
    {
        Program.Window = this;
        InitializeComponent();
    }
}
