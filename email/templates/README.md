# AuthorWings email templates

Nine transactional templates for a book publishing practice. All share one
header, footer and type system, so a client who gets a quote and later an
invoice sees the same brand both times.

| File | Send it when |
|---|---|
| `01-enquiry-auto-reply.html` | Someone submits the contact form. Sets expectations before a human replies. |
| `02-quote-estimate.html` | Quoting a project. Scope, per-service pricing, a total, and an expiry date. |
| `03-invoice.html` | Billing. Line items, tax, deposit already paid, amount due, pay button. |
| `04-payment-receipt.html` | Payment clears. Doubles as the client's receipt. |
| `05-payment-reminder.html` | An invoice is near or past due. Worded as a reminder, not a chase. |
| `06-project-update.html` | A milestone completes. Shows the whole pipeline, not just the latest step. |
| `07-proof-approval.html` | A cover or interior proof needs sign-off before print. |
| `08-consultation-confirmed.html` | A discovery call is booked. Time, joining link, what to bring. |
| `09-cost-estimate.html` | Someone completes the book cost calculator. Itemised breakdown, discount, estimated total. |
| `09-cost-estimate-demo.html` | The same email filled with a real calculator run, as a worked example. |

## Filling them in

Every editable string is wrapped in `{{ }}`. Search for `{{` and you will hit
all of them; nothing else needs touching. To check you have finished:

    grep -c '{{' 03-invoice.html      # should print 0 before you send

## The cost estimate

`09` is the email form of the calculator's PDF. The itemised rows are the
repeatable unit: duplicate one two-cell row per line. Keep the running
arithmetic honest, since the reader will add it up. In the worked example the
seventeen lines total $34,785, the LAUNCH1500 discount takes $1,485 off, and
the estimated total is $33,300.

The three notes under the total are not decoration. The sale's expiry and
exclusions, the rush surcharge, and the "guide estimate, not a binding
contract" line are what stop an estimate being read as a fixed price.

## Design system

| Token | Value | Used for |
|---|---|---|
| Green | `#5D7A6C` | Header bar, buttons, eyebrows, totals |
| Cream | `#F7F6F0` | Logo disc, wordmark on the green bar |
| Ink | `#2B2E26` | Headlines and body copy |
| Muted | `#6B6B6B` | Standfirsts, labels, secondary text |
| Hairline | `#E5DFD4` | Card border, rules, table dividers |
| Panel | `#F7F3EC` | Figure panels and detail blocks |

Green, cream and ink are sampled from the AuthorWings logo file rather than
picked by eye. The logo lockup's proportions are measured from it too: the
monogram's cap height is 0.352 of the disc, its width 0.850, the wordmark's
cap height 0.379, and the gap between mark and wordmark 0.352.

## Two typefaces, on purpose

Body copy is **Georgia**. Money, dates, phone numbers, labels and table
figures are **Arial**. That is not inconsistency: Georgia sets *old-style
figures*, where 3, 4, 7 and 9 drop below the baseline while 6 and 8 rise. In
running prose that is handsome; in an invoice total it looks broken. Keep
numbers in Arial.

## Fonts in the logo

The monogram and wordmark use Zilla Slab and PT Serif, subset to just the
letters they need and embedded as data URIs, so they need no network call.
Gmail's web client and Outlook desktop strip `@font-face` and will fall back
to Rockwell or Georgia. If you need the mark identical in every client, swap
the lockup for `../authorwings-header.png`, which `authorwings-email-template-image-logo.html`
shows how to do.

## Before sending a bulk send

`01` and `04`–`08` are transactional and exempt from CAN-SPAM's unsubscribe
requirement. If you reuse any of these shells for marketing, you must add a
postal address and a working unsubscribe link to the footer.
