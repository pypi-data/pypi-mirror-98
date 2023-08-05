def test_script_runner():

    import sys
    import json

    from hpb_mumc_dashboard.etl import script_runner

    with open('params.json', 'w') as f:
        json.dump({
            'scripts': [
                'DummyScript',
                'RetrieveStudyListScript',
                'RetrieveProcedureCountsAndComplicationsPerQuarterScript',
            ],
            'output_dir': '/tmp/hmd',
            'use_cache': True,
            'verbose': True,
        }, f, indent=4)

    sys.argv = ['script_runner.py', 'params.json']
    script_runner.main()
