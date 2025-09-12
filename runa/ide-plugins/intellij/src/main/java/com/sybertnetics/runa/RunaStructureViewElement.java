package com.sybertnetics.runa;

import com.intellij.ide.structureView.StructureViewTreeElement;
import com.intellij.ide.util.treeView.smartTree.SortableTreeElement;
import com.intellij.navigation.ItemPresentation;
import com.intellij.psi.NavigatablePsiElement;
import com.intellij.psi.PsiElement;
import org.jetbrains.annotations.NotNull;

import java.util.ArrayList;
import java.util.List;

/**
 * Structure view tree element for Runa language elements.
 */
public class RunaStructureViewElement implements StructureViewTreeElement, SortableTreeElement {
    
    private final PsiElement element;
    
    public RunaStructureViewElement(PsiElement element) {
        this.element = element;
    }
    
    @Override
    public Object getValue() {
        return element;
    }
    
    @Override
    public void navigate(boolean requestFocus) {
        if (element instanceof NavigatablePsiElement) {
            ((NavigatablePsiElement) element).navigate(requestFocus);
        }
    }
    
    @Override
    public boolean canNavigate() {
        return element instanceof NavigatablePsiElement &&
               ((NavigatablePsiElement) element).canNavigate();
    }
    
    @Override
    public boolean canNavigateToSource() {
        return element instanceof NavigatablePsiElement &&
               ((NavigatablePsiElement) element).canNavigateToSource();
    }
    
    @NotNull
    @Override
    public String getAlphaSortKey() {
        return element.getText();
    }
    
    @NotNull
    @Override
    public ItemPresentation getPresentation() {
        return new ItemPresentation() {
            @Override
            public String getPresentableText() {
                return element.getText();
            }
            
            @Override
            public String getLocationString() {
                return null;
            }
            
            @Override
            public javax.swing.Icon getIcon(boolean unused) {
                return RunaIcons.FILE;
            }
        };
    }
    
    @NotNull
    @Override
    public StructureViewTreeElement[] getChildren() {
        List<StructureViewTreeElement> children = new ArrayList<>();
        
        // Add child elements (simplified implementation)
        for (PsiElement child : element.getChildren()) {
            if (child instanceof RunaPsiElement) {
                children.add(new RunaStructureViewElement(child));
            }
        }
        
        return children.toArray(new StructureViewTreeElement[0]);
    }
}
