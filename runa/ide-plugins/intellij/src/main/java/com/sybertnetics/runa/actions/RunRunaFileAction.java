package com.sybertnetics.runa.actions;

import com.intellij.execution.ExecutionException;
import com.intellij.execution.configurations.GeneralCommandLine;
import com.intellij.execution.process.OSProcessHandler;
import com.intellij.execution.process.ProcessHandler;
import com.intellij.ide.util.PropertiesComponent;
import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.actionSystem.CommonDataKeys;
import com.intellij.openapi.editor.Editor;
import com.intellij.openapi.fileEditor.FileDocumentManager;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.ui.Messages;
import com.intellij.openapi.vfs.VirtualFile;
import com.sybertnetics.runa.RunaFileType;
import org.jetbrains.annotations.NotNull;

/**
 * Action to run Runa files using the Runa interpreter/runtime.
 */
public class RunRunaFileAction extends AnAction {
    
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
            runFile(project, file);
        } catch (Exception ex) {
            Messages.showErrorDialog(project, 
                "Failed to run Runa file: " + ex.getMessage(), 
                "Runtime Error");
        }
    }
    
    private void runFile(@NotNull Project project, @NotNull VirtualFile file) throws ExecutionException {
        // Get compiler/runtime path from settings
        PropertiesComponent properties = PropertiesComponent.getInstance(project);
        String runtimePath = properties.getValue(RUNA_COMPILER_PATH_KEY, DEFAULT_COMPILER_PATH);
        
        // Build command line
        GeneralCommandLine commandLine = new GeneralCommandLine();
        commandLine.setExePath(runtimePath);
        commandLine.addParameter("run");
        commandLine.addParameter(file.getPath());
        
        if (project.getBasePath() != null) {
            commandLine.setWorkDirectory(project.getBasePath());
        }
        
        // Execute program
        ProcessHandler processHandler = new OSProcessHandler(commandLine);
        processHandler.startNotify();
        
        // Show output in console (simplified implementation)
        Messages.showInfoMessage(project, 
            "Running: " + file.getName() + "\\nCheck console for output.", 
            "Runa Runtime");
    }
}
