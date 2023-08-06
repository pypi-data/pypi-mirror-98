=====
Usage
=====

To use justice in a project

.. code-block:: python

    from justice import Justice
    subject = Justice.search(string="Seznam CZ")
    # subject: dict({'file_number', 'ico', 'name', ...})
    detail = Justice.get_detail(subject_id=subject['subject_id'])
    # detail: dict({'Obchodní firma:', {'valid_from', 'valid_to', ...}})


To use from command line

.. code-block:: bash

    # Search company
    $ python -m justice.cli --search Seznam CZ
    [   {   'file_number': 'B 6493 vedená u Městského soudu v Praze',
        'ico': '26168685',
        'name': 'Seznam.cz, a.s.',
        'registration_date': '5. dubna 2000',
        'resistance': 'Radlická 3294/10, Smíchov, 150 00 Praha 5',
        'subject_id': '526277'},
    {   'file_number': 'C 209831 vedená u Městského soudu v Praze',
        'ico': '01673408',
        'name': 'Seznam.cz datová centra, s.r.o.',
        'registration_date': '15. května 2013',
        'resistance': 'Radlická 3294/10, Smíchov, 150 00 Praha 5',
        'subject_id': '429216'}]
    # Get company detail
    $ python -m justice.cli -g 526277
    [   (   'Obchodní firma:',
        'Seznam.cz, a.s.',
        {'valid_from': datetime.datetime(2000, 4, 5, 0, 0)})]
