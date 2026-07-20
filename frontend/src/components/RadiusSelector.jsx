const RADIUS_OPTIONS = [500, 1000, 1500];

function RadiusSelector({ radius, onChange }) {
    return (
        <div className="radius-selector">
            <p>검색 반경</p>

            <div className="radius-buttons">
                {RADIUS_OPTIONS.map((value) => (
                    <button
                        key={value}
                        type="button"
                        className={radius === value? "radius-button active" : "radius-button"}
                        onClick={() => onChange(value)}
                    >
                        {value}m
                    </button>
                ))}
            </div>
        </div>

    )

}

export default RadiusSelector;