# Advancement Chair Guide

Welcome! This guide walks you through the monthly advancement ceremony workflow and how to use the Scout Advancement Labels app. If you're taking over as advancement chair, this is everything you need to know.

## What This App Does

The Scout Advancement Labels app takes the purchase order CSV exported from Scoutbook and generates:

- **Printable labels** — stick on bags to identify each scout and their awards
- **Bagging guide** — a checklist with adventure loop/pin images so volunteers can bag the right items for each scout
- **Inventory tracking** — track leftover awards so you know what to buy vs what you already have

## What You Need

- A computer (macOS or Windows)
- Access to [Scoutbook Advancements](https://advancements.scouting.org/roster#advancements)
- Avery 6427 shipping labels (2" x 4", 10 per sheet) or compatible label sheets
- Snack-size zip bags (100 count) for bagging awards
- The Scout Advancement Labels app ([download latest release](https://github.com/Jasrags/scout-advancement/releases))

## Monthly Ceremony Workflow

### 1. Send Advancement Reminder (~1 week before ceremony)

Go to [Scoutbook Messaging](https://advancements.scouting.org/messaging) and send an email to den leaders:

- **Subject:** `[MONTH] Advancement Reminder`
- **Body:**

> Den leaders,
>
> This is your reminder that a pack performance is coming up on [DAY] ([DATE]), please ensure your advancements have been submitted to ScoutBook by end of [DAY] ([DATE]).
>
> Thank you!

### 2. Approve Advancements (Saturday/Sunday before ceremony)

Go to [Scoutbook Advancements](https://advancements.scouting.org/roster#advancements):

1. Click the **Advancements** tab
2. Go to **To Approve** — review and approve pending adventures and ranks
3. Go to **To Purchase** — click **Create Purchase Order** (or open an existing one)
4. Check items and add them to the purchase order

### 3. Download Documents

From the **To Purchase** tab:

1. Click **View Order** on your open purchase order
2. Click **Download CSV** — this is the file you'll load into the app
3. Download the **Purchase Order PDF** (for the scout shop)
4. Download the **Advancement Report PDF** (for the scout shop)

### 4. Email the Scout Shop

Send an email with both PDFs attached:

- **To:** Your local scout shop (e.g., 6115-LyleGambleScoutshop@scouting.org)
- **CC:** Your cubmaster
- **Subject:** `Pack [NUMBER] - Advancements`
- **Body:**

> I have attached the purchase orders and advancement reports for Pack [NUMBER]. We will need parent pins but we do not require pocket cards.
>
> I would like to pick up the materials Monday if possible.
>
> Thank you,
> [YOUR NAME]

If you've already checked inventory in the app (step 6), include a section listing items the shop does NOT need to pull because you already have them in stock.

### 5. Load CSV into the App

1. Open the Scout Advancement Labels app
2. Drag and drop your PO CSV file(s) onto the window, or click **Add Files...**
3. The app validates each file and shows the row count

### 6. Check Inventory (Optional)

If you've been tracking inventory:

1. Click **Check Inventory**
2. A table shows each award: how many you **Need**, how many you **Have**, and how many to **Buy**
3. Items you already have in stock are shown in **bold**
4. Use this info when emailing the scout shop (step 4) and when shopping (step 7)

### 7. Pick Up Awards

Go to the scout shop and purchase only what you need (the "Buy" column from the inventory check). Skip items you already have in stock.

### 8. Generate Labels and Bagging Guide

Back in the app:

1. Select your label type from the dropdown (default: Avery 6427)
2. Click **Settings...** to adjust label format if needed (name order, den number, etc.)
3. Click **Generate Labels PDF** — choose where to save, PDF opens automatically
4. Click **Generate Bagging Guide** — choose where to save, PDF opens automatically

### 9. Bag the Awards

Using the bagging guide:

1. Print the bagging guide
2. For each scout, gather the adventure loops/pins shown on their checklist
3. Check off each item as you bag it
4. Stick a label on each bag

### 10. Deduct from Inventory

After bagging is complete:

1. Click **Deduct from Inventory**
2. Review the confirmation dialog showing what will be subtracted
3. Click **Deduct** — inventory counts are updated

### 11. Ceremony Night

Hand out the labeled bags at the pack meeting. If a scout doesn't show up, keep their bag — add another label on top next month with any new awards.

### 12. Close the Purchase Order

Back in [Scoutbook](https://advancements.scouting.org/roster#advancements):

1. Go to **To Purchase** tab
2. Click **Close Order** on your purchase order
3. Items move to **To Award**, then mark them as **Awarded**

## Managing Inventory

The inventory screen lets you track leftover awards between ceremonies.

### Setting Up Inventory

1. Click **Manage Inventory** (always available, no CSV needed)
2. Each tab shows a rank (Lion through Arrow of Light)
3. Adventures are grouped: Required, Elective, Shooting Sports
4. Each card shows the adventure loop/pin image and name
5. Use **+/-** buttons to set how many you have of each
6. Click **Save** when done

### How Inventory Helps

- **Check Inventory** tells you what to buy vs what you already have
- **Deduct from Inventory** subtracts what you bagged after each ceremony
- At **end of year**, reconcile leftover bags — add unclaimed items back into inventory

## End of Year

At the end of the school year (or before the next year starts):

1. Open **Manage Inventory**
2. Review any leftover awards from scouts who left the pack or never picked up bags
3. Add unclaimed items back into inventory quantities
4. These carry over to the next year so you don't re-purchase them

## Tips

- **Multiple CSV files**: You can load multiple PO CSVs at once — the app combines them and deduplicates scouts automatically
- **Preview before printing**: Click **Preview** to see how your labels will look before generating the PDF
- **Label types**: If you use a different Avery label sheet, select it from the dropdown — the app supports several sizes
- **Scouts who miss ceremonies**: Keep their bag and add a new label next month. The old bag carries forward with new awards added on top.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Missing required column in CSV" | Verify your CSV has columns: `First Name`, `Last Name`, `Den Type`, `Den Number`, `Item Name` |
| Labels are too small / text is cut off | Try a larger label type (e.g., Avery 5164 at 3.33" x 4") |
| Adventure images not showing | Make sure the app was installed correctly with the `packaging/images/` directory |
| Inventory not saving | Check that the app has write access to your user data directory |

## Need Help?

- [GitHub Issues](https://github.com/Jasrags/scout-advancement/issues) — report bugs or request features
- [Scoutbook Help](https://help.scoutbook.scouting.org/knowledge-base/getting-a-unit-started-in-scoutbook/) — for Scoutbook-specific questions
- [Guide to Advancement](https://www.scouting.org/resources/guide-to-advancement/) — official BSA advancement policies
