package com.sybertnetics.runa;

import com.intellij.openapi.util.IconLoader;

import javax.swing.*;

/**
 * Icon definitions for the Runa plugin.
 */
public class RunaIcons {
    public static final Icon FILE = IconLoader.getIcon("/icons/runa-file.svg", RunaIcons.class);
    public static final Icon FUNCTION = IconLoader.getIcon("/icons/runa-function.svg", RunaIcons.class);
    public static final Icon VARIABLE = IconLoader.getIcon("/icons/runa-variable.svg", RunaIcons.class);
    public static final Icon TYPE = IconLoader.getIcon("/icons/runa-type.svg", RunaIcons.class);
    public static final Icon PROCESS = IconLoader.getIcon("/icons/runa-process.svg", RunaIcons.class);
    
    // Fallback to built-in icons if custom icons are not available
    public static final Icon FILE_FALLBACK = IconLoader.getIcon("/fileTypes/text.svg", RunaIcons.class);
    public static final Icon FUNCTION_FALLBACK = IconLoader.getIcon("/nodes/function.svg", RunaIcons.class);
    public static final Icon VARIABLE_FALLBACK = IconLoader.getIcon("/nodes/variable.svg", RunaIcons.class);
    public static final Icon TYPE_FALLBACK = IconLoader.getIcon("/nodes/class.svg", RunaIcons.class);
    
    private RunaIcons() {
        // Utility class
    }
}
