"""Views useful to other applications"""
from curriculum_model.db.schema import metadata

# Student numbers and gross fee income
FeeIncomeInputCostc = Table(
    'vFeeIncomeInputCostc', metadata,
    Column('Year', Integer),
    Column('CostC', CHAR(6)),
    Column('Income', DECIMAL(38, 7)),
    Column('usage_id', String(20)),
    Column('Session', Integer),
    Column('aos_code', CHAR(6)),
    Column('Students', DECIMAL(38, 5)),
    Column('Origin', String(11), nullable=False),
    Column('Fee Status', String(20))
)

# Hours of curriculum delivery
CurriculumEnrolsForAppTotal = Table(
    'vCurriculumEnrolsForAppTotal', metadata,
    Column('curriculum_id', Integer),
    Column('costc', CHAR(6)),
    Column('hours', Float(53))
)

# User friendly pivot of student numbers by costcentre, usage and year
SNInterfacePivot = Table(
    'vSNInterfacePivot', metadata,
    Column('primary_costc', CHAR(6, 'Latin1_General_CI_AS')),
    Column('acad_year', Integer),
    Column('usage_id', String(20, 'Latin1_General_CI_AS'), nullable=False),
    Column('primary_aos_code', CHAR(6, 'Latin1_General_CI_AS')),
    Column('fee_status', String(1, 'Latin1_General_CI_AS'), nullable=False),
    Column('set_cat_id', CHAR(3, 'Latin1_General_CI_AS'), nullable=False),
    Column('o_type', String(50, 'Latin1_General_CI_AS'), nullable=False),
    Column('Year 0', DECIMAL(38, 5)),
    Column('Year 1', DECIMAL(38, 5)),
    Column('Year 2', DECIMAL(38, 5)),
    Column('Year 3', DECIMAL(38, 5))
)
