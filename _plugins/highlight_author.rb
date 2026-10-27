# Liquid filter that wraps my name in rendered citations with <span class="me">.
# The name forms come from `highlight_names` in _config.yml. All forms are matched
# in one pass (longest first), and a form is skipped when more initials follow it,
# so "Truong, T." would never match a co-author such as "Truong, T. T.".
# An optional role (the `role` field in ref.bib) adds a marker after my name:
# † for co-first author, * for co-corresponding author.
module Jekyll
  module HighlightAuthorFilter
    ROLE_MARKS = { 'co-first' => '†', 'co-corresponding' => '*' }.freeze

    def highlight_author(input, role = nil)
      names = @context.registers[:site].config['highlight_names']
      return input if input.nil? || names.nil? || names.empty?

      mark = ROLE_MARKS[role.to_s.strip.downcase]
      mark = mark ? %(<sup class="role-mark" title="#{role.to_s.strip.capitalize} author">#{mark}</sup>) : ''
      alternation = names.sort_by { |n| -n.length }.map { |n| Regexp.escape(n) }.join('|')
      input.gsub(/(?<![\w-])(#{alternation})(?![\s-]*\p{Lu}\.)/) { %(<span class="me">#{$1}#{mark}</span>) }
    end
  end
end

Liquid::Template.register_filter(Jekyll::HighlightAuthorFilter)
