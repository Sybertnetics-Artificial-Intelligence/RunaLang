package com.sybertnetics.runa;

import com.intellij.formatting.*;
import com.intellij.lang.ASTNode;
import com.intellij.openapi.util.TextRange;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiFile;
import com.intellij.psi.codeStyle.CodeStyleSettings;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

/**
 * Formatting model builder for Runa language.
 * Provides automatic code formatting with proper indentation.
 */
public class RunaFormattingModelBuilder implements FormattingModelBuilder {
    
    @NotNull
    @Override
    public FormattingModel createModel(@NotNull FormattingContext formattingContext) {
        PsiElement element = formattingContext.getPsiElement();
        CodeStyleSettings settings = formattingContext.getCodeStyleSettings();
        
        return FormattingModelProvider.createFormattingModelForPsiFile(
            element.getContainingFile(),
            new RunaBlock(element.getNode(), null, Indent.getNoneIndent(), null, settings),
            settings
        );
    }
    
    @Nullable
    @Override
    public TextRange getRangeAffectingIndent(PsiFile file, int offset, ASTNode elementAtOffset) {
        return null;
    }
    
    private static class RunaBlock implements Block {
        private final ASTNode node;
        private final Alignment alignment;
        private final Indent indent;
        private final Wrap wrap;
        private final CodeStyleSettings settings;
        
        public RunaBlock(ASTNode node, Alignment alignment, Indent indent, Wrap wrap, CodeStyleSettings settings) {
            this.node = node;
            this.alignment = alignment;
            this.indent = indent;
            this.wrap = wrap;
            this.settings = settings;
        }
        
        @Override
        public ASTNode getNode() {
            return node;
        }
        
        @Override
        public TextRange getTextRange() {
            return node.getTextRange();
        }
        
        @NotNull
        @Override
        public java.util.List<Block> getSubBlocks() {
            java.util.List<Block> blocks = new java.util.ArrayList<>();
            ASTNode child = node.getFirstChildNode();
            
            while (child != null) {
                if (!child.getText().trim().isEmpty()) {
                    Indent childIndent = getChildIndent(child);
                    blocks.add(new RunaBlock(child, null, childIndent, null, settings));
                }
                child = child.getTreeNext();
            }
            
            return blocks;
        }
        
        private Indent getChildIndent(ASTNode child) {
            // Increase indent for block content
            String parentText = node.getText().trim();
            if (parentText.endsWith(":")) {
                return Indent.getNormalIndent();
            }
            return Indent.getNoneIndent();
        }
        
        @Nullable
        @Override
        public Wrap getWrap() {
            return wrap;
        }
        
        @Nullable
        @Override
        public Indent getIndent() {
            return indent;
        }
        
        @Nullable
        @Override
        public Alignment getAlignment() {
            return alignment;
        }
        
        @Nullable
        @Override
        public Spacing getSpacing(@Nullable Block child1, @NotNull Block child2) {
            return Spacing.createSpacing(0, 1, 0, true, 1);
        }
        
        @NotNull
        @Override
        public ChildAttributes getChildAttributes(int newChildIndex) {
            return new ChildAttributes(Indent.getNormalIndent(), null);
        }
        
        @Override
        public boolean isIncomplete() {
            return false;
        }
        
        @Override
        public boolean isLeaf() {
            return node.getFirstChildNode() == null;
        }
    }
}
