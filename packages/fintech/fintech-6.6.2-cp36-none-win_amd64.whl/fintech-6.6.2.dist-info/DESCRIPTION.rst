The Python FinTech package
==========================

This package contains all the functionality that is required to work with
EBICS, SEPA and other financial technologies. The usage has been realised
as simple as possible but also as flexible as necessary.

Features
--------

- Support of EBICS versions 2.4, 2.5 and 3.0
- Obtain bank account statements (incl. CAMT and MT940 parser)
- Create and submit SEPA credit transfers (pain.001)
- Create and submit SEPA direct debits CORE/B2B (pain.008)
- Mostly full SEPA support (including special schemes for CH and IT)
- Automatic calculation of the lead time based on holidays and cut-off times
- Integrated mandate manager (beta)
- Plausibility check of IBAN and BIC
- Validation of payment orders against the SEPA Clearing Directory of the
  German Central Bank
- Bankcode/Account to IBAN converter according to the rules of the German
  Central Bank
- Currency converter
- DATEV converter (CSV and KNE)

The FinTech package provides you the possibility to manage all of your everyday
commercial banking activities such as credit transfers, direct debits or the
retrieval of bank account statements in a flexible and secure manner.

All modules can be used free of charge. Only the unlicensed version of the
EBICS module has few restrictions. The upload of SEPA documents is limited
to a maximum of five transactions and bank account statements can not be
retrieved for the last three days.

Examples
--------

Simple SEPA Credit Transfer (pain.001)
++++++++++++++++++++++++++++++++++++++

.. sourcecode:: python

    import fintech
    fintech.register()
    from fintech.sepa import Account, SEPACreditTransfer

    # Create the debtor account from an IBAN
    debtor = Account('DE89370400440532013000', 'Max Mustermann')
    # Create the creditor account from a tuple (IBAN, BIC)
    creditor = Account(('AT611904300234573201', 'BKAUATWW'), 'Maria Musterfrau')
    # Create a SEPACreditTransfer instance
    sct = SEPACreditTransfer(debtor)
    # Add the transaction
    tx = sct.add_transaction(creditor, 10.00, 'Purpose')
    # Render the SEPA document
    print(sct.render())

Simple SEPA Direct Debit (pain.008)
+++++++++++++++++++++++++++++++++++

.. sourcecode:: python

    import fintech
    fintech.register()
    from fintech.sepa import Account, SEPADirectDebit

    # Create the creditor account from a tuple (ACCOUNT, BANKCODE)
    creditor = Account(('532013000', '37040044'), 'Max Mustermann')
    # Assign the creditor id
    creditor.set_creditor_id('DE98ZZZ09999999999')
    # Create the debtor account from a tuple (IBAN, BIC)
    debtor = Account(('AT611904300234573201', 'BKAUATWW'), 'Maria Musterfrau')
    # For a SEPA direct debit a valid mandate is required
    debtor.set_mandate(mref='M00123456', signed='2014-02-01', recurrent=True)
    # Create a SEPADirectDebit instance of type CORE
    sdd = SEPADirectDebit(creditor, 'CORE')
    # Add the transaction
    tx = sdd.add_transaction(debtor, 10.00, 'Purpose')
    # Render the SEPA document
    print(sdd.render())

EBICS
+++++

.. sourcecode:: python

    import fintech
    fintech.register()
    from fintech.ebics import EbicsKeyRing, EbicsBank, EbicsUser, EbicsClient

    keyring = EbicsKeyRing(keys='~/mykeys', passphrase='mysecret')
    bank = EbicsBank(keyring=keyring, hostid='MYBANK', url='https://www.mybank.de/ebics')
    user = EbicsUser(keyring=keyring, partnerid='CUSTOMER123', userid='USER1')
    # Create new keys for this user
    user.create_keys(keyversion='A006', bitlength=2048)

    client = EbicsClient(bank, user)
    # Send the public electronic signature key to the bank.
    client.INI()
    # Send the public authentication and encryption keys to the bank.
    client.HIA()

    # Create an INI-letter which must be printed and sent to the bank.
    user.create_ini_letter(bankname='MyBank AG', path='~/ini_letter.pdf')

    # After the account has been activated the public bank keys
    # must be downloaded and checked for consistency.
    print(client.HPB())

    # Finally the bank keys must be activated.
    bank.activate_keys()

    # Download CAMT53 bank account statements
    data = client.C53(
        start='2019-02-01',
        end='2019-02-07',
        )
    client.confirm_download()


Changelog
---------

v6.6.2 [2021-03-16]
    - CAMTParser: Fixed creditor/debtor assignment of reversed transactions.
    - DATEV: Group files by booking year and financial year.
    - DATEV: Reject amounts with more than two decimals.

v6.6.1 [2021-02-03]
    - Added missing SEPA countries AD and VC

v6.6.0 [2021-01-29]
    - Added support for Python 3.9

v6.5.2 [2020-12-06]
    - SEPA: Fixed bug parsing CAMT messages without AmtDtls node.
    - SEPA: Added SCL Card Clearing check to iban.check_bic().

v6.5.0 [2020-10-29]
    - EBICS: Added date range parameters to some download methods.
    - EBICS: Fixed missing TLS SNI support.
    - Dropped support for Python <2.7.9

v6.4.4 [2020-10-13]
    - EBICS: Added method EbicsBank.get_protocol_versions()
    - Fixed issue with Python 3.8

v6.4.1 [2020-07-30]
    - DATEV: Added support for divergent financial years.

v6.4.0 [2020-07-28]
    - EBICS: Added support for external signatures.
    - Added method LicenseManager.list_ebics_users()

v6.3.0 [2020-06-09]
    - DATEV: Added DatevCSV version 710.

v6.2.0 [2020-04-29]
    - SEPA: Added support for Instant Payments
    - SEPA: Added method Account.is_sepa()
    - SEPA: Fixed bug in Swiss SCT scheme versions
    - EBICS: Fixed issue with self-signed certificates
    - Fixed debugging issues

v6.1.1 [2019-12-24]
    - SEPA: Fixed bug in CBI scheme (CBI unique code)
    - SEPA: Added method Account.set_originator_id()

v6.1.0 [2019-12-19]
    - Added support for Python 3.8
    - Added currency of local account to SEPA documents
    - Changed LicenseManager endpoint

v6.0.7 [2019-09-21]
    - Added possibility to disable EBICS response verification.

v6.0.3 [2019-08-29]
    - Fixed Distributed Signature bug with key version A006.

v6.0.2 [2019-06-28]
    - Fixed creditor/debtor assignment of reversed transactions (CAMTParser).
    - Correctly sign amounts if reversal flag is set (MT940 parser).

v6.0.1 [2019-06-18]
    - EBICS: Implemented EBICS protocol version 3.0 (H005).
    - EBICS: Dropped support for PyCrypto.
    - EBICS: Removed depreciated factory function EbicsClientCompat.
    - EBICS: API changes: Renamed first parameter of EbicsClient.HVU()
      and EbicsClient.HVZ() from "ordertypes" to "filter".
    - SEPA: Added Swiss scheme versions.
    - SEPA: Added unstructured address attribute to Account.
    - SEPA: Updated IBAN countries.
    - DATEV: Added DatevCSV format.
    - Updated External Code Sets

v5.3.1 [2019-04-27]
    - SEPA: Fixed bug in CBI schemes

v5.3.0 [2019-04-09]
    - EBICS: Fixed bug downloading large files
    - SEPA: Added CBI schema for Italy

v5.2.1 [2019-03-03]
    - Fixed bug using a proxy.

v5.2.0 [2018-07-31]
    - Replaced the possibility to separate transactions with a method
      to create new batches.
    - Use INI letter path with user's home directory expanded.

v5.1.0 [2018-07-30]
    - Added possibility to process single transactions in its own batch.

v5.0.3 [2018-05-22]
    - Added FreeBSD binary

v5.0.2 [2018-04-03]
    - Fixed an issue with IPython and Django

v5.0.1 [2018-03-29]
    - Fixed VEU bug with suppress_no_data_error=True
    - Some code improvements

v5.0.0 [2018-03-26]
    - New packaging
    - Old versions should be uninstalled before upgrading!

v4.4.1 [2018-03-09]
    - Added some logging

v4.4.0 [2018-03-08]
    - Added EbicsClient context manager (auto-confirm)
    - Added EbicsClient property suppress_no_data_error
    - Added some IBAN countries
    - Fixed unverified SSL connections (Py>=2.7.9)
    - Accept multiple NtryDtls nodes in CAMTDocument

v4.3.5 [2017-10-25]
    - Fixed a SEPA date issue.
    - MT940 parser: Accept all characters in purpose text even if defined as delimiter.
    - Fixed a distributed signature bug.

v4.3.4 [2017-08-10]
    - Added the fields *sum_credits* and *sum_debits* to the MT942 parser.
    - Fixed the handling of invalid times (24:00:00) in CAMT documents.
    - Added the possibility to specify custom order parameters for FDL/FUL.
    - Added further support for SEPA structured references.

v4.3.3 [2017-06-06]
    - Fixed a bug parsing CAMT52 documents.
    - Made the user for EbicsClient optional.
    - Fixed a bug in EbicsUser.create_ini_letter to correctly return bytes.
    - Added silent parameter to method EbicsBank.activate_keys.
    - Added the attributes reference_id and sequence_id to the CAMTDocument parser.
    - Now parses the transaction classification also for DK in addition to ZKA.

v4.3.2 [2017-03-30]
    - Minor bug fix parsing MT942 documents.
    - Minor bug fix creating self-signed certificates.
    - Fixed a problem with Python builts compiled without "--with-fpectl".

v4.3.1 [2017-02-06]
    - Fixed a bug of Account.set_mandate with named arguments.

v4.3.0 [2017-01-19]
    - PyOpenSSL is not longer required to support certificates.
    - Removed direct debit type COR1 and adjusted mandate sequence types.
      API changes:

      - OLD: Account.set_mandate(mref, signed, first, last)
      - NEW: Account.set_mandate(mref, signed, recurrent)
      - OLD: SEPADirectDebit(account, 'COR1', ...)
      - NEW: SEPADirectDebit(account, 'CORE', ...)

v4.2.4 [2017-01-17]
    - Added a check for DigestMethod algorithm.
    - Fixed a bug rejecting mandates signed more than three years ago.
    - Fixed minor bug in mt940 parser.

v4.2.3 [2016-10-27]
    - Fixed bug of wrong content type in EBICS module.
    - Added support for EBICS uploads that are approved manually via accompanying document.

v4.2.2 [2016-05-05]
    - Added timeout to EBICS requests.
    - Made BIC optional for SEPA transactions.
    - Added creditor id to InitgPty/OrgId for Spanish banks.
    - Added postal address to SEPA documents.
    - Added support for creditor reference numbers.

v4.2.1 [2015-08-20]
    - Added a check of the unicode variant (UCS2, UCS4) to setup.py.

v4.2.0 [2015-08-17]
    - Added the SEPA fields BREF, RREF, SQTP and RTCD to the MT940 parser.
    - Added a dictionary of possible return codes to the SEPA module.
    - Added the possibility to dynamically license additional EBICS users.
    - Fixed an encoding bug of non-ascii error messages under Python 2.
    - Fixed a bug swapping local and remote account for returned transactions
      by the CAMT parser.

v4.1.1 [2015-04-24]
    - Disabled output of license due to some difficulties with pip

v4.1.0 [2015-04-20]
    - Added support for other currencies in addition to EUR.
    - Added new Amount class with an integrated currency converter.
    - Now the SEPATransaction property *amount* is of type Amount.

v4.0.0 [2015-04-14]
    - Made the library Python 2/3 compatible.
    - Added support for the cryptography package in addition to PyCrypto.
    - Made the BIC optional for national transactions.
    - Added the originator id to SEPA documents in GB and IE.
    - Added a check to recognize transaction duplicates.
    - Added a CAMT parser.
    - Changed some attributes of SEPATransaction instances to be conform
      with the new CAMT parser:

      + Removed the property *id*.
      + Removed the property *account*, instead use the method *get_account()*.
      + Renamed the property *due_date* to *date*.
      + Renamed the property *ext_purpose* to *purpose_code*.
      + Changed the property *purpose*, now it is a tuple of strings.
      + Changed the property *amout*, now debits are signed negative.

    - Fixed the handling of invalid dates (eg. 2015-02-30) in MT940 and
      CAMT parsers.
    - Fixed a problem with the exception handling in IPython.
    - Some code improvements and minor bug fixes.

v3.0.3 [2015-02-05]
    - Fixed a bug in the XML to dictionary converter.
    - Fixed a bug in the path handler of the EbicsKeyRing class.

v3.0.2 [2015-01-29]
    - Fixed a bug handling bank keys with a small bit-length.
    - Added some tolerance to the MT940 parser and collect unknown structured
      fields.

v3.0.1 [2015-01-26]
    - Renamed the package from *ebics* to *fintech* and the module *client* to
      *ebics*.
    - Splitted the functionality of the class *EbicsClient* into the classes
      *EbicsClient*, *EbicsBank*, *EbicsUser* and *EbicsKeyRing*. Added the
      new class factory *EbicsClientCompat* for backwards compatibility.
    - Added basic support for EBICS protocol version 2.4 (H003).
    - Added support for certificates.
    - Added the order types FUL and FDL.
    - Added a French and English version of the INI-letter.
    - Added the order types PUB, HCA, HCS and H3K.
    - Added a check of remote SSL certificates against trusted CAs.
    - Fixed the broken functionality of distributed signatures.
    - Added a much faster PBKDF2 implementation.
    - Created a more tolerant MT940 parser.
    - Changed the API of *SEPACreditTransfer* and *SEPADirectDebit* to be more
      consistent and added support for different PAIN scheme versions.
    - Several bug fixes.

v2.1.2 [2014-10-26]
    - Fixed some bugs regarding the distributed signature

v2.1.1 [2014-10-26]
    - Fixed a bug throwing an exception in an unregistered version of PyEBICS.
    - Fixed bug of wrong *OrderParams* tag used by orders of the distributed
      signature.

v2.1.0 [2014-09-29]
    - Added some functionality based on the SCL Directory, published by the
      German Central Bank.

v2.0.3 [2014-09-11]
    - Fixed a bug refusing valid creditor ids.
    - Added a test to check DATEV parameters for invalid arguments.

v2.0.2 [2014-09-05]
    - Fixed a bug in some EBICS requests (missing parameter tag).
    - Fixed a bug in the MT940 parser.

v2.0.1 [2014-08-18]
    - Fixed a bug handling XML namespaces.
    - Changed the behaviour of the flag *parsed* of some methods. Now a
      structure of dictionaries is returned instead of an objectified XML
      object.
    - Changed the expected type of the *params* parameter. Now it must be
      a dictionary instead of a list of tuples.
    - Added support for distributed signatures (HVU, HVD, HVZ, HVT, HVE, HVS).

v1.3.0 [2014-07-29]
    - Fixed a few minor bugs.
    - Made the package available for Windows.

v1.2.0 [2014-05-23]
    - Added new DATEV module.
    - Fixed wrong XML position of UltmtCdtr node in SEPA documents.
    - Changed the order of the (BANKCODE, ACCOUNT) tuple to (ACCOUNT, BANKCODE)
      used by the Account initializer.

v1.1.25 [2014-02-22]
    - Minor bug fix of the module loader.

v1.1.24 [2014-02-21]
    - First public release.


