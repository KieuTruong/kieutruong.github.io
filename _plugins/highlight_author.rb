# Liquid filter that wraps my name in rendered citations with <span class="me">.
# The name forms come from `highlight_names` in _config.yml. All forms are matched
# in one pass (longest first), and a form is skipped when more initials follow it,
# so "Truong, T." would never match a co-author such as "Truong, T. T.".
module Jekyll
  module HighlightAuthorFilter
    def highlight_author(input)
      names = @context.registers[:site].config['highlight_names']
      return input if input.nil? || names.nil? || names.empty?

      alternation = names.sort_by { |n| -n.length }.map { |n| Regexp.escape(n) }.join('|')
      input.gsub(/(?<![\w-])(#{alternation})(?![\s-]*\p{Lu}\.)/) { %(<span class="me">#{$1}</span>) }
    end
  end
end

Liquid::Template.register_filter(Jekyll::HighlightAuthorFilter)
