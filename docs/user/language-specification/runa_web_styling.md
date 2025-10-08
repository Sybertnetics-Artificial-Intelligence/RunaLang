# Runa Web Styling Specification (Aether Framework)

**Version:** 1.0
**Status:** Canonical - Aether Framework
**Last Updated:** 2025-10-08

---

## Overview

**Runa replaces CSS with executable `.runa` style files.**

**Replaces:**
- ❌ CSS
- ❌ SCSS/Sass
- ❌ Less
- ❌ Styled-components
- ❌ Tailwind CSS

---

## Basic Styles

**File:** `styles.runa`

```runa
Note: Web styling in Runa (Aether Framework)
Note: Replaces CSS/SCSS

Import "runa/aether/styles" as Style

Process called "define_styles" returns Style.Stylesheet:
    Return Style.stylesheet(
        Style.rule(".container", a dictionary containing:
            "max-width" as "1200px",
            "margin" as "0 auto",
            "padding" as "20px"
        End Dictionary),

        Style.rule(".button", a dictionary containing:
            "background-color" as "#007bff",
            "color" as "white",
            "padding" as "10px 20px",
            "border" as "none",
            "border-radius" as "4px",
            "cursor" as "pointer"
        End Dictionary),

        Style.rule(".button:hover", a dictionary containing:
            "background-color" as "#0056b3"
        End Dictionary)
    )
End Process

Let STYLES be define_styles()
```

---

## CSS Comparison

**Before (styles.css):**
```css
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.button:hover {
  background-color: #0056b3;
}
```

**After (styles.runa):**
```runa
Let styles be Style.create(
    rule(".container", props("max-width", "1200px", "margin", "0 auto", "padding", "20px")),
    rule(".button", props(
        "background-color", "#007bff",
        "color", "white",
        "padding", "10px 20px",
        "border-radius", "4px"
    )),
    rule(".button:hover", props("background-color", "#0056b3"))
)
```

---

## Computed Styles

```runa
Process called "theme_colors" that takes theme as String returns Dictionary[String, String]:
    Return match theme:
        When "light":
            a dictionary containing:
                "primary" as "#007bff",
                "background" as "#ffffff",
                "text" as "#000000"
            End Dictionary
        When "dark":
            a dictionary containing:
                "primary" as "#0056b3",
                "background" as "#1a1a1a",
                "text" as "#ffffff"
            End Dictionary
        Otherwise:
            theme_colors("light")
    End Match
End Process

Process called "create_themed_styles" that takes theme as String returns Style.Stylesheet:
    Let colors be theme_colors(theme)

    Return Style.stylesheet(
        Style.rule("body", a dictionary containing:
            "background-color" as colors at key "background",
            "color" as colors at key "text"
        End Dictionary),

        Style.rule(".button-primary", a dictionary containing:
            "background-color" as colors at key "primary"
        End Dictionary)
    )
End Process
```

---

## Responsive Design

```runa
Process called "responsive_styles" returns Style.Stylesheet:
    Return Style.stylesheet(
        Style.rule(".grid", a dictionary containing:
            "display" as "grid",
            "grid-template-columns" as "repeat(3, 1fr)",
            "gap" as "20px"
        End Dictionary),

        Style.media_query("max-width: 768px",
            Style.rule(".grid", a dictionary containing:
                "grid-template-columns" as "repeat(2, 1fr)"
            End Dictionary)
        ),

        Style.media_query("max-width: 480px",
            Style.rule(".grid", a dictionary containing:
                "grid-template-columns" as "1fr"
            End Dictionary)
        )
    )
End Process
```

---

## Component Styles

```runa
Process called "Button" that takes text as String, variant as String returns Web.Element:
    Let button_styles be match variant:
        When "primary":
            props("background-color", "#007bff", "color", "white")
        When "secondary":
            props("background-color", "#6c757d", "color", "white")
        When "danger":
            props("background-color", "#dc3545", "color", "white")
        Otherwise:
            props("background-color", "#e0e0e0", "color", "#000000")
    End Match

    Return Web.button(text, Style.inline(button_styles))
End Process
```

---

## SCSS Comparison

**Before (styles.scss):**
```scss
$primary-color: #007bff;
$padding-small: 10px;
$padding-large: 20px;

.button {
  background-color: $primary-color;
  padding: $padding-small $padding-large;

  &:hover {
    background-color: darken($primary-color, 10%);
  }

  &.large {
    padding: $padding-large * 1.5;
  }
}
```

**After (styles.runa):**
```runa
Constant PRIMARY_COLOR as String is "#007bff"
Constant PADDING_SMALL as Integer is 10
Constant PADDING_LARGE as Integer is 20

Process called "button_styles" returns Style.Stylesheet:
    Return Style.stylesheet(
        rule(".button", props(
            "background-color", PRIMARY_COLOR,
            "padding", string_from(PADDING_SMALL) + "px " + string_from(PADDING_LARGE) + "px"
        )),

        rule(".button:hover", props(
            "background-color", darken(PRIMARY_COLOR, 10)
        )),

        rule(".button.large", props(
            "padding", string_from(PADDING_LARGE * 3 / 2) + "px"
        ))
    )
End Process

Process called "darken" that takes color as String, percent as Integer returns String:
    Note: Color manipulation function
    Return Style.adjust_color(color, "darken", percent)
End Process
```

---

## Animations

```runa
Process called "define_animations" returns Style.Stylesheet:
    Return Style.stylesheet(
        Style.keyframes("fade-in", a list containing:
            keyframe(0, props("opacity", "0")),
            keyframe(100, props("opacity", "1"))
        End),

        Style.rule(".fade-in", a dictionary containing:
            "animation" as "fade-in 0.3s ease-in"
        End Dictionary)
    )
End Process

Process called "keyframe" that takes percent as Integer, properties as Dictionary[String, String] returns Dictionary[String, Any]:
    Return a dictionary containing:
        "offset" as percent,
        "properties" as properties
    End Dictionary
End Process
```

---

## Utility Functions

```runa
Process called "props" that takes pairs as Variadic[String] returns Dictionary[String, String]:
    Let result be an empty dictionary

    Let i be 0
    While i < length of pairs:
        Let key be pairs at index i
        Let value be pairs at index (i + 1)
        Set result at key key to value
        Set i to i + 2
    End While

    Return result
End Process

Process called "spacing" that takes size as Integer returns String:
    Return string_from(size * 4) + "px"
End Process

Process called "color_with_alpha" that takes hex as String, alpha as Float returns String:
    Return Style.hex_to_rgba(hex, alpha)
End Process
```

---

## Tailwind-Style Utilities

```runa
Process called "utility_classes" returns Style.Stylesheet:
    Return Style.stylesheet(
        rule(".flex", props("display", "flex")),
        rule(".flex-col", props("flex-direction", "column")),
        rule(".justify-center", props("justify-content", "center")),
        rule(".items-center", props("align-items", "center")),
        rule(".gap-1", props("gap", spacing(1))),
        rule(".gap-2", props("gap", spacing(2))),
        rule(".gap-4", props("gap", spacing(4))),
        rule(".p-1", props("padding", spacing(1))),
        rule(".p-2", props("padding", spacing(2))),
        rule(".m-1", props("margin", spacing(1))),
        rule(".m-2", props("margin", spacing(2)))
    )
End Process
```

---

## Summary

**Runa replaces CSS/SCSS with:**
- ✅ Type-safe styling
- ✅ Computed values
- ✅ Theme support
- ✅ Component-scoped styles
- ✅ No preprocessors needed

**Stop using:** CSS, SCSS, Tailwind
**Start using:** Aether Styling (`.runa`)

---

**End of Document**
