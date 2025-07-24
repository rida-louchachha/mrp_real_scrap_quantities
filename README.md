==========================================

MRP Scrap \& Real Quantity Enhancement

==========================================



This module extends the Manufacturing (MRP) functionality in Odoo to allow better tracking and management of component scrap, visual quantity, and actual consumption during the production process.



Key Features

============



\- Introduces new fields on Bill of Materials lines:

&nbsp; - \*\*Visual Quantity\*\*: Expected quantity before scrap.

&nbsp; - \*\*Scrap Quantity\*\*: Estimated scrap amount.

&nbsp; - \*\*Real Quantity\*\*: Computed as `Visual - Scrap`.

&nbsp; - \*\*Usage Percent\*\*: Scrap percentage of visual quantity.



\- Automatically updates manufacturing raw material moves (`stock.move`) with:

&nbsp; - \*\*Visual Quantity\*\*

&nbsp; - \*\*Scrap Quantity\*\*

&nbsp; - \*\*Real Quantity\*\*

&nbsp; - Updates `product\_uom\_qty` to reflect \*\*real quantity\*\* in MO context.



\- Adds logic to:

&nbsp; - Create scrap `stock.move.line` during production completion (`button\_mark\_done`).

&nbsp; - Prevent duplication of scrap move lines.

&nbsp; - Dynamically compute consumption factors when changing quantities to produce.



\- Report Enhancements:

&nbsp; - Adds \*\*Visual Qty\*\*, \*\*Real Qty\*\*, \*\*Scrap Qty\*\*, and \*\*Scrap %\*\* columns to the manufacturing order report (`mrp.report\_mrporder`).

&nbsp; - Enhances the component table in the report (`report\_mrp\_production\_components`).



Benefits

========



\- More accurate reporting of real consumed material.

\- Clear separation between planned and lost material during manufacturing.

\- Improved scrap traceability in stock move lines.

\- Enhanced transparency for production efficiency and costing.



Technical Details

=================



\- Inherits and extends the following models:

&nbsp; - `mrp.production`

&nbsp; - `stock.move`

&nbsp; - `mrp.bom.line`



\- Adds logic in:

&nbsp; - `\_get\_moves\_raw\_values`

&nbsp; - `button\_mark\_done`

&nbsp; - `\_onchange` methods for reactive updates

&nbsp; - Stock move computation to support `real\_qty`



\- Fully integrated with:

&nbsp; - Odoo MRP workflows

&nbsp; - Manufacturing order reports

&nbsp; - Scrap handling in `stock.location`



Installation

============



1\. Copy the module to your Odoo `addons` directory.

2\. Update the app list.

3\. Install the module via Odoo UI or using command line:

&nbsp;  ```bash

&nbsp;  odoo -u your\_module\_name

3\. Install the module from the Apps interface.



Author \& Contact

================

Author: Rida Louchachha  

Email: ridalouchachha2580@gmail.com

