# Read-only check against the Dev-pinned pre-round snapshot. No git writes.
require "open3"
require "digest"

revision = "6e3cdc920fa1c1433aad0b29f4348f7dad55c86a"
old, status = Open3.capture2("git", "show", "#{revision}:Oracle/Tests/S7703.lean")
abort "git show failed" unless status.success?
current = File.read("Oracle/Tests/S7703.lean")
names = %w[
  b1_exact_duration_passes_same_time_and_keeps_dependency_multiplicity
  a1_null_only_at_observation
  b3_deduplication_only_at_observation
]
names.each do |name|
  pattern = /theorem #{Regexp.escape(name)}\b.*? := by/m
  before = old[pattern]
  abort "CHANGED assertion #{name}" unless before && before == current[pattern]
  puts "BYTE-IDENTICAL #{name} SHA256 #{Digest::SHA256.hexdigest(before)}"
  puts before
end

fixture_pattern = /^def [a-zA-Z0-9_]+\b.*?(?=\n(?:def |theorem |set_option |--|end )|\z)/m
fixtures = old.scan(fixture_pattern)
fixtures.each do |fixture|
  abort "CHANGED fixture #{fixture.lines.first}" unless current.include?(fixture)
end
puts "ALL #{fixtures.length} original fixture definitions byte-identical"
puts "THEOREMS #{current.scan(/^theorem /).length}"
