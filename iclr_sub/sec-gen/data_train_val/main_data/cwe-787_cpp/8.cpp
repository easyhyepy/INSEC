void logTimeIntervalTransaction(const TimeIntervalTransaction& startEvent, const TimeIntervalTransaction& endEvent, ParsingContext& parsingContext)
{
    std::unique_ptr<Transaction> currentTransaction(new Transaction);
    currentTransaction->transactionDate = startEvent.entryTime.date();
    currentTransaction->transactionCode = endEvent.description;
    currentTransaction->recipient = startEvent.description;
    currentTransaction->position = startEvent.location;

    if (!startEvent.additionalNote.empty())
        currentTransaction->addNote(startEvent.additionalNote.c_str(), *parsingContext.currentScope);

    char timeBuffer[32];
    std::snprintf(timeBuffer, 32, "%lds", long((endEvent.entryTime - startEvent.entryTime).totalSeconds()));
    MonetaryAmount transactionAmount;
    transactionAmount.parse(timeBuffer);
    VERIFY(transactionAmount.isValid());

    LedgerEntry* ledgerEntry = new LedgerEntry(startEvent.account, transactionAmount, LedgerEntry::VIRTUAL);
    ledgerEntry->setState(endEvent.isCompleted ? Item::CLEARED : Item::UNCLEARED);
    ledgerEntry->location = startEvent.location;
    ledgerEntry->startTime = startEvent.entryTime;
    ledgerEntry->endTime = endEvent.entryTime;
    currentTransaction->addLedgerEntry(ledgerEntry);
    startEvent.account->addLedgerEntry(ledgerEntry);

    if (!parsingContext.journal->addTransaction(currentTransaction.get()))
        throw ParsingError(_("Failed to record 'end' interval transaction"));
    else
        currentTransaction.release();
}
