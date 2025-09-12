package com.sybertnetics.runa;

import com.intellij.lang.cacheBuilder.DefaultWordsScanner;
import com.intellij.lang.cacheBuilder.WordsScanner;
import com.intellij.lang.findUsages.FindUsagesProvider;
import com.intellij.psi.PsiElement;
import com.intellij.psi.tree.TokenSet;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

/**
 * Find usages provider for Runa language elements.
 */
public class RunaFindUsagesProvider implements FindUsagesProvider {
    
    @Nullable
    @Override
    public WordsScanner getWordsScanner() {
        return new DefaultWordsScanner(
            new RunaLexer(),
            TokenSet.create(RunaTokenTypes.IDENTIFIER),
            TokenSet.create(RunaTokenTypes.COMMENT),
            TokenSet.create(RunaTokenTypes.STRING_LITERAL)
        );
    }
    
    @Override
    public boolean canFindUsagesFor(@NotNull PsiElement psiElement) {
        return psiElement instanceof RunaPsiElement;
    }
    
    @Nullable
    @Override
    public String getHelpId(@NotNull PsiElement psiElement) {
        return null;
    }
    
    @NotNull
    @Override
    public String getType(@NotNull PsiElement element) {
        return "Runa element";
    }
    
    @NotNull
    @Override
    public String getDescriptiveName(@NotNull PsiElement element) {
        return element.getText();
    }
    
    @NotNull
    @Override
    public String getNodeText(@NotNull PsiElement element, boolean useFullName) {
        return element.getText();
    }
}
