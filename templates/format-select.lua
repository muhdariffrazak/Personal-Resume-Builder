-- Drops Divs marked .latex-only / .docx-only when the current writer doesn't
-- match, so one generated Markdown file can carry format-specific header
-- markup for both the PDF (LaTeX) and DOCX builds without duplicating content.
function Div(el)
  if el.classes:includes("latex-only") and FORMAT ~= "latex" then
    return {}
  end
  if el.classes:includes("docx-only") and FORMAT ~= "docx" then
    return {}
  end
  return el
end
