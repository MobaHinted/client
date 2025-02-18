// MobaHinted Copyright (C) 2025 Ethan Henderson <ethan@zbee.codes>
// Licensed under GPLv3 - Refer to the LICENSE file for the complete text

#region

using Avalonia.Controls;

#endregion

namespace client.Views;

public partial class LaunchView : Window, Iview
{
    public LaunchView()
    {
        Program.Window = this;
        InitializeComponent();
    }
}
