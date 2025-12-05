import React, { useState } from 'react';
import { Button } from '@/components/livekit/button';

function WelcomeLogo() {
  return (
    <div className="relative mb-6 flex items-center justify-center">
      {/* Outer ocean glow */}
      <div className="absolute h-24 w-24 rounded-full bg-gradient-to-tr from-sky-500/40 via-cyan-400/30 to-emerald-300/40 blur-xl" />

      {/* Inner badge */}
      <div className="relative flex h-16 w-16 items-center justify-center rounded-2xl border border-cyan-400/80 bg-slate-950/90 shadow-[0_0_30px_rgba(56,189,248,0.7)]">
        {/* Shark fin icon */}
        <svg
          viewBox="0 0 64 64"
          className="h-10 w-10 text-cyan-300 drop-shadow-[0_0_14px_rgba(56,189,248,0.95)]"
          fill="currentColor"
        >
          <path d="M8 50C10 46 15 40 22 36C27 33 32 32 35 32C35 26 37 18 43 11C44 9.5 46 9 47.5 10C53 14 57 22 56 34C55.5 40.5 54 46 52.5 50H8Z" />
          <path d="M10 44C15 43 21 43 26 44C30 45 33 47 35 49H12C11 49 10.2 48.5 10 47.5C9.8 46.5 9.5 45.2 10 44Z" />
        </svg>
      </div>
    </div>
  );
}

function CornerEmoji({ className, children }: { className?: string; children: React.ReactNode }) {
  return (
    <div
      className={
        'pointer-events-none select-none drop-shadow-[0_0_18px_rgba(34,197,235,0.6)] ' +
        (className ?? '')
      }
    >
      {children}
    </div>
  );
}

export const WelcomeView = React.forwardRef<HTMLDivElement, any>(
  ({ startButtonText, onStartCall, ...rest }, ref) => {
    const [name, setName] = useState('');
    const [started, setStarted] = useState(false);

    const buttonLabel = startButtonText || 'Pitch the Shark';

    async function handleStart() {
      const trimmed = name.trim();
      if (!trimmed) return;
      setStarted(true);
      onStartCall?.(trimmed);
    }

    return (
      <div
        ref={ref}
        {...rest}
        className="min-h-screen w-full flex flex-col justify-center items-center md:items-end md:pr-24 lg:pr-32 bg-transparent text-white"
      >
        {!started && (
          <section
            className="
              relative flex flex-col items-center text-center p-8
              w-full max-w-sm mx-4 md:mx-0
              rounded-3xl overflow-hidden
              bg-slate-950/90 border border-slate-800/70
              shadow-[0_0_60px_rgba(15,23,42,0.98)]
              backdrop-blur-2xl
            "
          >
            {/* Ocean / tank glow */}
            <div className="pointer-events-none absolute -inset-16 bg-[radial-gradient(circle_at_top,_rgba(56,189,248,0.35)_0,_transparent_55%),radial-gradient(circle_at_bottom,_rgba(45,212,191,0.3)_0,_transparent_55%)]" />

            {/* Corner emojis for Shark Tank vibe */}
            <CornerEmoji className="absolute top-5 left-6 text-3xl -rotate-8">
              🦈
            </CornerEmoji>
            <CornerEmoji className="absolute top-6 right-7 text-2xl rotate-4">
              💼
            </CornerEmoji>
            <CornerEmoji className="absolute bottom-6 left-6 text-2xl rotate-3">
              💰
            </CornerEmoji>
            <CornerEmoji className="absolute bottom-5 right-7 text-2xl -rotate-6">
              📊
            </CornerEmoji>

            {/* Logo / shark icon */}
            <WelcomeLogo />

            {/* Title & subtitle */}
            <div className="relative z-10">
              <p className="mb-1 text-[11px] font-semibold uppercase tracking-[0.22em] text-cyan-300/80">
                Shark Tank AI
              </p>
              <h2 className="text-2xl font-extrabold text-slate-50 mb-2 tracking-tight drop-shadow-[0_0_18px_rgba(15,23,42,0.9)]">
                Enter the Tank
              </h2>
              <p className="max-w-prose text-sm leading-6 font-medium text-slate-300">
                Drop your startup name and let the AI shark grill your pitch, rip apart the weak spots,
                and help you sharpen it like a real investor predator.
              </p>
            </div>

            {/* Name input + start button */}
            <div className="mt-8 w-full relative z-10">
              <label className="block text-xs font-bold uppercase tracking-[0.18em] mb-2 text-left text-slate-400 ml-1">
                Your Startup Name
              </label>

              <div className="flex w-full items-stretch gap-2">
                <input
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') handleStart();
                  }}
                  placeholder="SharkTech Labs, Royal Ventures, etc..."
                  className="
                    flex-1 rounded-xl border border-slate-700/70 px-4 py-3
                    bg-slate-950/80 text-slate-50 placeholder:text-slate-500
                    font-semibold
                    shadow-[inset_0_0_0_1px_rgba(15,23,42,0.9)]
                    focus:outline-none focus:ring-2 focus:ring-cyan-400/80 focus:border-cyan-300/80
                    transition-all duration-200
                  "
                />

                <Button
                  variant="primary"
                  size="default"
                  onClick={handleStart}
                  disabled={!name.trim()}
                  className="
                    px-4 md:px-5 rounded-xl font-bold uppercase text-[11px]
                    bg-gradient-to-r from-cyan-400 via-sky-500 to-emerald-400
                    text-slate-950 border-none
                    shadow-[0_0_32px_rgba(56,189,248,0.9)]
                    hover:from-cyan-300 hover:via-sky-400 hover:to-emerald-300
                    disabled:opacity-60 disabled:cursor-not-allowed
                    flex items-center gap-2 justify-center
                    transform hover:scale-[1.03] active:scale-[0.98] transition-all
                  "
                >
                  <span>{buttonLabel}</span>
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                    className="size-4"
                  >
                    <path
                      fillRule="evenodd"
                      d="M4 12.75A.75.75 0 0 1 4.75 12H17.19l-3.22-3.22a.75.75 0 1 1 1.06-1.06l4.5 4.5a.76.76 0 0 1 .16.24.75.75 0 0 1-.16.82l-4.5 4.5a.75.75 0 1 1-1.06-1.06L17.19 13.5H4.75A.75.75 0 0 1 4 12.75Z"
                      clipRule="evenodd"
                    />
                  </svg>
                </Button>
              </div>
            </div>

            <div className="mt-4 text-[10px] text-slate-400 font-mono uppercase tracking-[0.24em] relative z-10">
              Press Enter to Face the Shark
            </div>
          </section>
        )}

        {started && (
          <div className="text-center text-slate-50 text-2xl font-bold animate-pulse md:pr-12 drop-shadow-[0_0_20px_rgba(15,23,42,1)]">
            🦈 Sharpening its teeth… get ready to be grilled.
          </div>
        )}
      </div>
    );
  },
);

WelcomeView.displayName = 'WelcomeView';
