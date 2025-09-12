package com.sybertnetics.runa.actions;

import com.intellij.execution.ExecutionException;
import com.intellij.execution.configurations.GeneralCommandLine;
import com.intellij.execution.process.OSProcessHandler;
import com.intellij.execution.process.ProcessHandler;
import com.intellij.execution.ui.ConsoleView;
import com.intellij.execution.ui.ConsoleViewContentType;
import com.intellij.ide.util.PropertiesComponent;
import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.actionSystem.CommonDataKeys;
import com.intellij.openapi.editor.Editor;
import com.intellij.openapi.fileEditor.FileDocumentManager;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.ui.Messages;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.openapi.wm.ToolWindow;
import com.intellij.openapi.wm.ToolWindowManager;
import com.sybertnetics.runa.RunaFileType;
import org.jetbrains.annotations.NotNull;

import java.io.File;

/**
 * Action to compile Runa files using the Runa compiler.
 */
public class CompileRunaFileAction extends AnAction {
    
    private static final String RUNA_COMPILER_PATH_KEY = "runa.compiler.path";
    private static final String DEFAULT_COMPILER_PATH = "runa";
    
    @Override
    public void update(@NotNull AnActionEvent e) {
        // Only enable for Runa files
        VirtualFile file = e.getData(CommonDataKeys.VIRTUAL_FILE);
        boolean isRunaFile = file != null && 
                           file.getFileType() instanceof RunaFileType;
        e.getPresentation().setEnabledAndVisible(isRunaFile);
    }
    
    @Override
    public void actionPerformed(@NotNull AnActionEvent e) {
        Project project = e.getProject();
        VirtualFile file = e.getData(CommonDataKeys.VIRTUAL_FILE);
        Editor editor = e.getData(CommonDataKeys.EDITOR);
        
        if (project == null || file == null) {
            return;
        }
        
        // Save the file first
        if (editor != null) {
            FileDocumentManager.getInstance().saveDocument(editor.getDocument());
        }
        
        try {
            compileFile(project, file);
        } catch (Exception ex) {
            Messages.showErrorDialog(project, 
                "Failed to compile Runa file: " + ex.getMessage(), 
                "Compilation Error");
        }
    }
    
    private void compileFile(@NotNull Project project, @NotNull VirtualFile file) throws ExecutionException {
        // Get compiler path from settings
        PropertiesComponent properties = PropertiesComponent.getInstance(project);
        String compilerPath = properties.getValue(RUNA_COMPILER_PATH_KEY, DEFAULT_COMPILER_PATH);
        
        // Check if compiler exists
        if (!isCompilerAvailable(compilerPath)) {
            int result = Messages.showYesNoDialog(project,
                "Runa compiler not found at: " + compilerPath + "\\n" +
                "Would you like to configure the compiler path?",
                "Compiler Not Found",
                Messages.getQuestionIcon());
            
            if (result == Messages.YES) {
                String newPath = Messages.showInputDialog(project,
                    "Enter the path to the Runa compiler:",
                    "Configure Runa Compiler",
                    Messages.getQuestionIcon(),
                    compilerPath,
                    null);
                
                if (newPath != null && !newPath.trim().isEmpty()) {
                    properties.setValue(RUNA_COMPILER_PATH_KEY, newPath.trim());
                    compilerPath = newPath.trim();
                } else {
                    return;
                }
            } else {
                return;
            }
        }
        
        // Build command line
        GeneralCommandLine commandLine = new GeneralCommandLine();
        commandLine.setExePath(compilerPath);
        commandLine.addParameter("compile");
        commandLine.addParameter(file.getPath());
        
        if (project.getBasePath() != null) {
            commandLine.setWorkDirectory(project.getBasePath());
        }
        
        // Execute compilation
        ProcessHandler processHandler = new OSProcessHandler(commandLine);
        
        // Get or create console view
        ConsoleView console = getConsoleView(project);
        if (console != null) {
            console.clear();
            console.print("Compiling: " + file.getName() + "\\n", ConsoleViewContentType.NORMAL_OUTPUT);
            console.print("Command: " + commandLine.getCommandLineString() + "\\n\\n", ConsoleViewContentType.SYSTEM_OUTPUT);
            
            // Attach console to process
            console.attachToProcess(processHandler);
        }
        
        // Start the process
        processHandler.startNotify();
        
        // Show console tool window
        ToolWindowManager toolWindowManager = ToolWindowManager.getInstance(project);
        ToolWindow toolWindow = toolWindowManager.getToolWindow("Run");
        if (toolWindow != null) {
            toolWindow.activate(null);
        }
    }
    
    private boolean isCompilerAvailable(String compilerPath) {
        try {
            File compilerFile = new File(compilerPath);
            if (compilerFile.exists() && compilerFile.canExecute()) {
                return true;
            }
            
            // Try to execute it to see if it's in PATH
            ProcessBuilder pb = new ProcessBuilder(compilerPath, "--version");
            Process process = pb.start();
            int exitCode = process.waitFor();
            return exitCode == 0;
        } catch (Exception e) {
            return false;
        }
    }
    
    private ConsoleView getConsoleView(@NotNull Project project) {
        // This is a simplified implementation
        // In a full implementation, you would create or reuse a proper console view
        return null;
    }
}
