# Guide: `write_file` (boot.dev — Write Files)

No solution code here. Just the order to do things in, and a checkpoint after each
step so you always know whether you're done.

Time: ~20 minutes. Step 1 is the unblock — do it first even if you stop after.

---

## Where you are right now

`functions/write_file_content.py` exists, but its body is a **verbatim copy of
`get_files_info.py`**. It references a variable `directory` that no longer exists
in the signature, so the file cannot run. That's the whole reason it feels stuck:
you're not looking at a blank page, you're looking at 25 lines of *wrong* code,
which is worse.

The good news: about half of what's in there is already correct. You've written
the path-validation block twice before and it's the same block here.

---

## Step 1 — Make it run (5 min)

Open `functions/write_file_content.py`.

1. Replace every `directory` with `file_path` (lines 9, 15, 18).
2. Delete lines 20–25 — the `results = []` loop and the `"\n".join(results)`
   return. It's leftover from the directory listing function and does nothing
   for you here.

**Checkpoint:** the file imports without a `NameError`. Try it:

```
uv run python -c "from functions.write_file_content import write_file; print(write_file('calculator', 'x.txt', 'hi'))"
```

It will still be wrong. That's fine. It *runs*.

---

## Step 2 — Fix the two error strings (3 min)

Two `return f'Error: ...'` lines survived the copy-paste with the wrong wording.
The assignment gives you both strings exactly. Copy them character-for-character
— the boot.dev CLI test compares them literally, so a stray word will fail an
otherwise-correct function.

One of the two also has an **inverted condition**:

- `get_files_info` wanted: "this must BE a directory, else error"
- `write_file` wants: "this must NOT be a directory, else error"

Same `os.path.isdir()` call, opposite branch.

**Checkpoint:** re-read your two error strings against the assignment text
side by side. Then run the same one-liner from Step 1 — you should now get the
directory-related error message or fall through, not a listing.

---

## Step 3 — The one genuinely new part (5 min)

Everything so far you'd written before. This bit you haven't.

Before you can open a file for writing, its **parent directory has to exist**.
`write_file("calculator", "pkg/morelorem.txt", ...)` will fail if `calculator/pkg/`
isn't there — Python won't create it for you.

Two functions from the assignment's Tips list, used together in one line:

- one gives you the **parent directory** of a path
- one **creates a directory tree**, and takes an argument that makes it a no-op
  when the directory already exists

Neither appears anywhere else in your `functions/` directory. That's your hint
that this is the new material.

Place it **after** the validation checks and **before** the write. Order matters:
you don't want to create directories for a path you're about to reject.

**Checkpoint:** ask yourself — if `calculator/pkg/` already exists, does your
line blow up? If you used the right argument, no.

---

## Step 4 — Actually write the file (2 min)

The assignment hands you this snippet outright. You also already have the read
version in `get_file_content.py:21` — it's the same shape with a different mode
and `.write()` instead of `.read()`.

Then return the success string. Copy it exactly; it uses `len(content)`.

**Why a success string and not `None`?** This function is a tool for an LLM. The
model only knows the write worked because you told it so in text it can read.
Silent success is invisible to the agent. That's the "feedback loops" line in the
assignment, and it's the actual lesson of this exercise.

**Checkpoint:** run the one-liner from Step 1 again. You should get
`Successfully wrote to "x.txt" (2 characters written)` and a real
`calculator/x.txt` on disk. Delete it afterwards.

---

## Step 5 — The test module (5 min)

Create `test_write_file.py` at the **project root** (not in `functions/`), next to
`test_get_file_content.py`. Open that file and copy its structure — import, three
calls, print each result.

The three cases from the assignment, and what each one is checking:

| Call | What it proves |
|---|---|
| `("calculator", "lorem.txt", ...)` | plain write into the working dir |
| `("calculator", "pkg/morelorem.txt", ...)` | Step 3 worked — nested path |
| `("calculator", "/tmp/temp.txt", ...)` | the sandbox holds — absolute path escapes |

That third one is the interesting case. Think about *why* an absolute path like
`/tmp/temp.txt` gets rejected by your existing validation block — what does
`os.path.join()` do when the second argument starts with `/`? Trace it by hand
before you run it. It's the subtlest behaviour in this whole exercise and it's
doing real security work for you.

**Checkpoint:** three printed lines — two successes, one
`Error: Cannot write to "/tmp/temp.txt" ...`. And **no file at `/tmp/temp.txt`**.
Check that; a passing print with a written file would mean the guard leaked.

---

## Step 6 — Submit

Run the boot.dev CLI test and submit.

---

## Stuck on a specific step?

Say which step number and paste the error. Don't restart from scratch — the steps
are independent enough that you can fix one without touching the others.

---

## Optional, after you've passed — don't do this first

You've now written this block three times:

```
abspath → join → normpath → commonpath → compare
```

Worth thinking about (there's no single right answer):

- Extract it into a shared helper in `functions/`? Less duplication, one place to
  fix a security bug.
- Leave it? Three copies is where duplication *starts* to hurt, and the error
  message differs in each ("Cannot list" / "Cannot read" / "Cannot write"), so a
  helper needs a parameter for that.

boot.dev doesn't require it. Get the exercise passing first — a refactor before
the tests go green is just a second way to be stuck.
