-- Applies the typographic scale (see templates/resume.latex) to custom-style
-- Divs on the PDF/LaTeX build. The docx build gets its sizing from the
-- matching named styles in templates/reference.docx instead -- this filter
-- only needs to do anything when FORMAT == "latex".
local SIZE_COMMAND = {
  ResumeName = "\\namesize",
  EntryHeader = "\\entryheadersize",
}

function Div(el)
  local size_cmd = SIZE_COMMAND[el.attributes["custom-style"]]
  if FORMAT == "latex" and size_cmd then
    for _, block in ipairs(el.content) do
      if block.t == "Para" or block.t == "Plain" then
        table.insert(block.content, 1, pandoc.RawInline("latex", "{" .. size_cmd .. " "))
        table.insert(block.content, pandoc.RawInline("latex", "}"))
      end
    end
  end
  return el
end
