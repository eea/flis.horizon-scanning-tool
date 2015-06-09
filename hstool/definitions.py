DOC_TYPE_CHOICES = (
    (1, 'Trends'),
    (2, 'Uncertainties'),
    (3, 'Wild Cards'),
    (4, 'Weak signals')
)

DOC_TREND_TYPE_CHOICES = (
    (1, 'Trend'),
    (2, 'Megatrend'),
)

DOC_UNCERTAINTIES_TYPE_CHOICES = (
    (1, 'Rationale'),
    (2, 'Data'),
    (3, 'Methodology (related to the model)'),
)

DOC_STEEP_CHOICES = (
    ('Ec', 'Economic'),
    ('Env', 'Environmental'),
    ('P', 'Political'),
    ('S', 'Social'),
    ('T', 'Technological'),
)

DOC_TIME_HORIZON_CHOICES = (
    (1, '1 year'),
    (5, '5 years'),
    (10, '10 years'),
    (50, '50 years'),
    (100, '100 years'),
    (200, 'more than 100 years'),
)

IND_TIMELINE_CHOICES = (
    (5, '5-year intermediate'),
    (0, 'continuous'),
    (1, 'daily'),
    (2, 'monthly'),
    (3, 'point'),
    (4, 'weekly'),
    (6, 'yearly'),
)

RELATION_TYPE_CHOICES = (
    (1, 'Cause-effect relationship'),
    (2, 'Neutral relationship'),
)

CANONICAL_ROLES = (
    'Authenticated',
    'Administrator',
    'Contributor',
    'Viewer',
    'Reviewer',
)
