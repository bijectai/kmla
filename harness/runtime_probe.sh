#!/bin/sh
# Only infrastructure measurements; no corpus or semantic transformations.
set -eu
printf 'version_string\t'; swipl --version
printf 'plarch\t'; swipl --dump-runtime-variables | sed -n 's/^PLARCH="\(.*\)";$/\1/p'
printf 'plversion\t'; swipl --dump-runtime-variables | sed -n 's/^PLVERSION="\(.*\)";$/\1/p'
printf 'uname_m\t'; uname -m
printf 'dpkg_arch\t'; dpkg --print-architecture
printf 'tz\t%s\n' "$TZ"
printf 'tz_sha256\t'; sha256sum "/usr/share/zoneinfo/$TZ" | cut -d ' ' -f 1
printf 'winter_offset\t'; swipl -q -f none -g "format_time(atom(A),'%z',1483228800),writeln(A),halt"
printf 'summer_offset\t'; swipl -q -f none -g "format_time(atom(A),'%z',1498867200),writeln(A),halt"

# Observe the actual Prolog process, not the client's CPU or Docker settings.
swipl -q -f none -g 'writeln(runtime_probe_ready),flush_output,sleep(30),halt' >/tmp/runtime-ready &
pid=$!
trap 'kill "$pid" 2>/dev/null || true; wait "$pid" 2>/dev/null || true' EXIT
attempt=0
while [ ! -s /tmp/runtime-ready ]; do
    kill -0 "$pid"
    attempt=$((attempt + 1))
    [ "$attempt" -le 100 ] || exit 2
    sleep 0.1
done
printf 'process_exe\t'; readlink "/proc/$pid/exe"
printf 'process_exe_sha256\t'; sha256sum "/proc/$pid/exe" | cut -d ' ' -f 1
printf 'process_elf_machine\t'; od -An -tx1 -j18 -N2 "/proc/$pid/exe" | tr -d ' \n'; printf '\n'
printf 'swipl_exe\t'; readlink -f /usr/bin/swipl
printf 'swipl_exe_sha256\t'; sha256sum /usr/bin/swipl | cut -d ' ' -f 1
