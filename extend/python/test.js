function test() {
  try {
    const poUpdates = [];
    const PO_INDEX = 2;
    const DATE_INDEX = 3;
    const VENDOR_INDEX = 1;
    const DESCRIPTION_INDEX = 5;
    const INVOICE_NUMBER_INDEX = 4;
    const ROW_INDEX = 12;
    const updated_pos = [];
    const MAX_LIMIT = 10;
    let processedCount = 0;
    const poMap = {};
    poUpdates.forEach((row) => {
      try {
        const po = row[PO_INDEX];
        const date = row[DATE_INDEX];
        const invoice = row[INVOICE_NUMBER_INDEX];
        const vendor = row[VENDOR_INDEX];
        const description = row[DESCRIPTION_INDEX];
        if (po) {
          poMap[po] = {
            date: date,
            invoice: invoice,
            description: vendor + "-" + description,
            index: row[ROW_INDEX],
          };
        }
      } catch (mapError) {
        console.error("Error building poMap:", mapError);
      }
    });
    const poInputs = document.querySelectorAll(
      "input[id^='PurchParmTable_PurchId'][id$='_input']",
    );
    for (const poInput of poInputs) {
      if (processedCount >= MAX_LIMIT) {
        console.log("Reached processing limit:", MAX_LIMIT);
        break;
      }
      try {
        const poValue = poInput.value.trim();
        if (poMap[poValue]) {
          const row =
            poInput.closest("[role='row']") ||
            poInput.closest("tr") ||
            poInput.parentElement?.parentElement?.parentElement;
          if (!row) continue;
          const nativeSetter = Object.getOwnPropertyDescriptor(
            HTMLInputElement.prototype,
            "value",
          ).set;
          const dateInput = row.querySelector("input[arial-label='Date']");
          if (dateInput && poMap[poValue].date) {
            dateInput.focus();
            dateInput.click();
            nativeSetter.call(dateInput, poMap[poValue].date);
            dateInput.dispatchEvent(new Event("input", { bubbles: true }));
            dateInput.dispatchEvent(new Event("change", { bubbles: true }));
          }
          const invoiceInput = row.querySelector(
            "input[arial-label='Invoice Number']",
          );
          if (invoiceInput && poMap[poValue].invoice) {
            invoiceInput.focus();
            invoiceInput.click();
            nativeSetter.call(invoiceInput, poMap[poValue].invoice);
            invoiceInput.dispatchEvent(new Event("input", { bubbles: true }));
            invoiceInput.dispatchEvent(new Event("change", { bubbles: true }));
          }
          const dateVAT = row.querySelector(
            "input[arial-label='Date of VAT register']",
          );
          if (dateVAT && poMap[poValue].date) {
            dateVAT.focus();
            dateVAT.click();
            nativeSetter.call(dateVAT, poMap[poValue].date);
            dateVAT.dispatchEvent(new Event("input", { bubbles: true }));
            dateVAT.dispatchEvent(new Event("change", { bubbles: true }));
          }
          const invoiceReceivedDate = row.querySelector(
            "input[arial-label='Invoice received date']",
          );
          if (invoiceReceivedDate && poMap[poValue].date) {
            invoiceReceivedDate.focus();
            invoiceReceivedDate.click();
            nativeSetter.call(invoiceReceivedDate, poMap[poValue].date);
            invoiceReceivedDate.dispatchEvent(
              new Event("input", { bubbles: true }),
            );
            invoiceReceivedDate.dispatchEvent(
              new Event("change", { bubbles: true }),
            );
          }
          const invoiceDate = row.querySelector(
            "input[arial-label='Invoice date']",
          );
          if (invoiceDate && poMap[poValue].date) {
            invoiceDate.focus();
            invoiceDate.click();
            nativeSetter.call(invoiceDate, poMap[poValue].date);
            invoiceDate.dispatchEvent(new Event("input", { bubbles: true }));
            invoiceDate.dispatchEvent(new Event("change", { bubbles: true }));
          }
          const description = row.querySelector(
            "input[arial-label='Invoice description']",
          );
          if (description && poMap[poValue].description) {
            description.focus();
            description.click();
            nativeSetter.call(description, poMap[poValue].description);
            description.dispatchEvent(new Event("input", { bubbles: true }));
            description.dispatchEvent(new Event("change", { bubbles: true }));
          }
          updated_pos.push({
            po: poValue,
            date: poMap[poValue].date,
            invoice: poMap[poValue].invoice,
            status: "updated",
            index: poMap[poValue].index,
          });
          processedCount++;
          console.log(`Updated (${processedCount}/${MAX_LIMIT}) PO ${poValue}`);
        }
      } catch (innerError) {
        console.error("Error processing PO:", innerError);
        updated_pos.push({
          po: poInput?.value || null,
          status: "error",
          error: innerError.message,
        });
      }
    }
    const last3Values = Array.from(poInputs)
      .slice(-3)
      .map((input) => input.value.trim());
    updated_pos.push(last3Values);
    return updated_pos;
  } catch (error) {
    console.error("Fatal error:", error);
    return [{ status: "fatal_error", error: error.message }];
  }
}
